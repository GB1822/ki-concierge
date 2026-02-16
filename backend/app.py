#!/usr/bin/env python3
"""
KI-CONCIERGE Backend API
Micro-SaaS Chatbot mit automatischem Crawling & PDF-Parsing
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# LangChain & AI Imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader, PyPDFLoader, TextLoader
from langchain.memory import ConversationBufferMemory

# Crawling & Processing
import requests
from bs4 import BeautifulSoup
import pdfplumber

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="KI-CONCIERGE API",
    description="Intelligenter Website-Chatbot mit automatischem Crawling",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: restrict to your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class WebsiteConfig(BaseModel):
    """Configuration for website crawling"""
    url: str
    max_pages: int = 50
    include_pdfs: bool = True
    include_docs: bool = True

class ChatMessage(BaseModel):
    """Chat message from user"""
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    """Response from chatbot"""
    response: str
    session_id: str
    sources: List[str] = []
    confidence: float = 0.0

class TrainingRequest(BaseModel):
    """Request to train on new documents"""
    website_url: str
    pdf_urls: List[str] = []
    doc_urls: List[str] = []
    api_key: str

# In-memory storage (in production: use Redis/DB)
vector_stores = {}
conversation_memories = {}
website_configs = {}

# API Key validation (simplified)
def validate_api_key(api_key: str = Header(...)):
    """Validate API key"""
    # In production: check against database
    if not api_key.startswith("kc_"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "KI-CONCIERGE API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/train - Train chatbot on website",
            "/chat - Chat with trained bot",
            "/config - Update configuration",
            "/status - Check training status"
        ]
    }

@app.post("/train")
async def train_chatbot(request: TrainingRequest):
    """
    Train chatbot on a website and documents
    """
    try:
        logger.info(f"Starting training for website: {request.website_url}")
        
        # Step 1: Crawl website
        documents = await crawl_website(request.website_url, request.max_pages)
        
        # Step 2: Process PDFs
        if request.pdf_urls:
            pdf_docs = await process_pdfs(request.pdf_urls)
            documents.extend(pdf_docs)
        
        # Step 3: Process other documents
        if request.doc_urls:
            doc_docs = await process_documents(request.doc_urls)
            documents.extend(doc_docs)
        
        # Step 4: Create embeddings and vector store
        vector_store = await create_vector_store(documents, request.api_key)
        
        # Step 5: Store configuration
        website_configs[request.api_key] = {
            "website_url": request.website_url,
            "trained_at": datetime.now().isoformat(),
            "document_count": len(documents),
            "pdf_count": len(request.pdf_urls)
        }
        
        vector_stores[request.api_key] = vector_store
        
        return {
            "status": "success",
            "message": f"Chatbot trained on {len(documents)} documents",
            "website": request.website_url,
            "documents_processed": len(documents),
            "pdfs_processed": len(request.pdf_urls)
        }
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.post("/chat")
async def chat_with_bot(
    message: ChatMessage,
    api_key: str = Depends(validate_api_key)
):
    """
    Chat with trained chatbot
    """
    try:
        if api_key not in vector_stores:
            raise HTTPException(status_code=404, detail="Chatbot not trained. Please train first.")
        
        # Get or create conversation memory
        if message.session_id not in conversation_memories:
            conversation_memories[message.session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        
        memory = conversation_memories[message.session_id]
        vector_store = vector_stores[api_key]
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
            chain_type="stuff",
            retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
            memory=memory,
            return_source_documents=True
        )
        
        # Get response
        result = qa_chain({"query": message.message})
        
        # Extract sources
        sources = []
        if "source_documents" in result:
            for doc in result["source_documents"]:
                if hasattr(doc, 'metadata') and 'source' in doc.metadata:
                    sources.append(doc.metadata['source'])
        
        return ChatResponse(
            response=result["result"],
            session_id=message.session_id,
            sources=list(set(sources))[:3],  # Limit to 3 unique sources
            confidence=0.85  # Placeholder
        )
        
    except Exception as e:
        logger.error(f"Chat failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.get("/config/{api_key}")
async def get_config(api_key: str):
    """Get chatbot configuration"""
    if api_key not in website_configs:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    return website_configs[api_key]

@app.post("/config/{api_key}")
async def update_config(api_key: str, config: WebsiteConfig):
    """Update chatbot configuration"""
    website_configs[api_key] = config.dict()
    return {"status": "success", "message": "Configuration updated"}

# Helper functions
async def crawl_website(url: str, max_pages: int = 50) -> List[Any]:
    """Crawl website and extract content"""
    logger.info(f"Crawling website: {url}")
    
    try:
        # Simple crawling - in production use Scrapy or specialized crawler
        loader = WebBaseLoader([url])
        documents = loader.load()
        
        # Limit pages
        documents = documents[:max_pages]
        
        logger.info(f"Crawled {len(documents)} pages from {url}")
        return documents
        
    except Exception as e:
        logger.error(f"Website crawling failed: {str(e)}")
        return []

async def process_pdfs(pdf_urls: List[str]) -> List[Any]:
    """Process PDF documents"""
    documents = []
    
    for pdf_url in pdf_urls:
        try:
            logger.info(f"Processing PDF: {pdf_url}")
            
            # Download PDF
            response = requests.get(pdf_url)
            pdf_path = f"/tmp/{os.path.basename(pdf_url)}"
            
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            
            # Extract text from PDF
            loader = PyPDFLoader(pdf_path)
            pdf_docs = loader.load()
            
            # Add metadata
            for doc in pdf_docs:
                doc.metadata["source"] = pdf_url
                doc.metadata["type"] = "pdf"
            
            documents.extend(pdf_docs)
            logger.info(f"Processed PDF: {pdf_url} - {len(pdf_docs)} pages")
            
        except Exception as e:
            logger.error(f"PDF processing failed for {pdf_url}: {str(e)}")
    
    return documents

async def process_documents(doc_urls: List[str]) -> List[Any]:
    """Process text documents"""
    documents = []
    
    for doc_url in doc_urls:
        try:
            logger.info(f"Processing document: {doc_url}")
            
            # Download document
            response = requests.get(doc_url)
            doc_path = f"/tmp/{os.path.basename(doc_url)}"
            
            with open(doc_path, 'wb') as f:
                f.write(response.content)
            
            # Extract text based on file type
            if doc_url.endswith('.txt'):
                loader = TextLoader(doc_path)
                doc_docs = loader.load()
            else:
                # Try to extract text anyway
                with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                from langchain.schema import Document
                doc_docs = [Document(page_content=content, metadata={"source": doc_url, "type": "document"})]
            
            documents.extend(doc_docs)
            logger.info(f"Processed document: {doc_url}")
            
        except Exception as e:
            logger.error(f"Document processing failed for {doc_url}: {str(e)}")
    
    return documents

async def create_vector_store(documents: List[Any], api_key: str):
    """Create vector store from documents"""
    if not documents:
        raise ValueError("No documents to process")
    
    logger.info(f"Creating vector store from {len(documents)} documents")
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    splits = text_splitter.split_documents(documents)
    logger.info(f"Split into {len(splits)} chunks")
    
    # Create embeddings
    embeddings = OpenAIEmbeddings()
    
    # Create vector store (in production: use Pinecone/Weaviate)
    vector_store = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        collection_name=f"ki_concierge_{api_key}"
    )
    
    logger.info("Vector store created successfully")
    return vector_store

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )