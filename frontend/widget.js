            return new Promise((resolve) => {
                setTimeout(() => {
                    const responses = {
                        en: {
                            'hello': "Hello! I'm your AI assistant. I can help answer questions about this website. What would you like to know?",
                            'price': "KI-CONCIERGE costs €29-99/month. The Professional plan (€59/month) is most popular and includes unlimited crawling, 50 PDFs, and priority support.",
                            'features': "I can crawl websites automatically, read PDFs, answer questions based on your content, and adapt to your brand colors. No manual training needed!",
                            'integration': "Integration takes 30 seconds: Just add a JavaScript snippet before </body>. No coding skills required!",
                            'pdf': "Yes, I can read PDFs! Upload price lists, catalogs, or whitepapers - I'll extract the text and answer questions about them.",
                            'default': "I'm an AI chatbot that automatically learns from websites and PDFs. I can answer customer questions 24/7 and adapt to your brand design. Want to know more about pricing, integration, or features?"
                        },
                        de: {
                            'hallo': "Hallo! Ich bin dein KI-Assistent. Ich kann Fragen zu dieser Website beantworten. Was möchtest du wissen?",
                            'preis': "KI-CONCIERGE kostet €29-99/Monat. Der Professional Plan (€59/Monat) ist am beliebtesten und beinhaltet unbegrenztes Crawling, 50 PDFs und Priority Support.",
                            'funktionen': "Ich kann Websites automatisch crawlen, PDFs lesen, Fragen zu deinen Inhalten beantworten und mich an deine Markenfarben anpassen. Kein manuelles Training nötig!",
                            'integration': "Integration dauert 30 Sekunden: Einfach JavaScript Snippet vor </body> einfügen. Keine Coding-Kenntnisse benötigt!",
                            'pdf': "Ja, ich kann PDFs lesen! Lade Preislisten, Kataloge oder Whitepapers hoch - ich extrahiere den Text und beantworte Fragen dazu.",
                            'default': "Ich bin ein KI-Chatbot der automatisch von Websites und PDFs lernt. Ich beantworte Kundenfragen 24/7 und passe mich an dein Corporate Design an. Möchtest du mehr über Preise, Integration oder Features wissen?"
                        }
                    };
                    
                    const lang = this.language;
                    const lowerMessage = message.toLowerCase();
                    const langResponses = responses[lang] || responses.en;
                    
                    for (const [key, response] of Object.entries(langResponses)) {
                        if (lowerMessage.includes(key)) {
                            resolve(response);
                            return;
                        }
                    }
                    
                    resolve(langResponses.default);
                }, 1000 + Math.random() * 1000); // Simulate network delay
            });
        }
        
        // Public API methods
        open() {
            this.open();
        }
        
        close() {
            this.close();
        }
        
        sendMessage(text) {
            if (text) {
                this.inputField.value = text;
                this.sendMessage();
            }
        }
        
        updateConfig(newConfig) {
            this.config = { ...this.config, ...newConfig };
            
            // Update language if changed
            if (newConfig.language) {
                this.language = newConfig.language === 'auto' ? detectLanguage() : newConfig.language;
                
                // Update UI texts
                this.updateUITexts();
            }
            
            // Update colors if changed
            if (newConfig.primaryColor) {
                this.updateColors();
            }
        }
        
        updateUITexts() {
            // Update toggle button title
            this.toggleButton.title = this.isOpen ? t('close') : t('open');
            
            // Update input placeholder
            this.inputField.placeholder = t('placeholder');
            
            // Update send button
            const sendButton = this.chatWindow.querySelector('button[title]');
            if (sendButton) {
                sendButton.textContent = t('send');
                sendButton.title = t('send');
            }
            
            // Update close button
            const closeButton = this.chatWindow.querySelector('button[title="×"]');
            if (closeButton) {
                closeButton.title = t('close');
            }
            
            // Update footer
            const footer = this.chatWindow.querySelector('div:last-child');
            if (footer) {
                footer.innerHTML = `${t('poweredBy')} <strong>KI-Strategen.eu</strong>`;
            }
        }
        
        updateColors() {
            // Update toggle button
            this.toggleButton.style.background = this.config.primaryColor;
            
            // Update header
            const header = this.chatWindow.querySelector('div:first-child');
            if (header) {
                header.style.background = this.config.primaryColor;
            }
            
            // Update send button
            const sendButton = this.chatWindow.querySelector('button:not([title="×"])');
            if (sendButton) {
                sendButton.style.background = this.config.primaryColor;
            }
        }
        
        getMessages() {
            return [...this.messages];
        }
        
        clearMessages() {
            this.messages = [];
            this.messagesContainer.innerHTML = '';
            this.addMessage({
                text: this.config.welcomeMessage,
                sender: 'bot',
                timestamp: new Date()
            });
        }
    }
    
    // Global API
    window.KIConcierge = {
        init(config = {}) {
            if (!window._kiConciergeInstance) {
                window._kiConciergeInstance = new KIConciergeWidget(config);
            }
            return window._kiConciergeInstance;
        },
        
        open() {
            if (window._kiConciergeInstance) {
                window._kiConciergeInstance.open();
            }
        },
        
        close() {
            if (window._kiConciergeInstance) {
                window._kiConciergeInstance.close();
            }
        },
        
        sendMessage(text) {
            if (window._kiConciergeInstance) {
                window._kiConciergeInstance.sendMessage(text);
            }
        },
        
        updateConfig(config) {
            if (window._kiConciergeInstance) {
                window._kiConciergeInstance.updateConfig(config);
            }
        },
        
        getMessages() {
            if (window._kiConciergeInstance) {
                return window._kiConciergeInstance.getMessages();
            }
            return [];
        },
        
        clearMessages() {
            if (window._kiConciergeInstance) {
                window._kiConciergeInstance.clearMessages();
            }
        },
        
        // Helper function for translation
        t(key, lang = null) {
            return t(key, lang);
        }
    };
    
    // Auto-initialize if config is present
    if (window.kiConciergeConfig) {
        window.addEventListener('DOMContentLoaded', () => {
            window.KIConcierge.init(window.kiConciergeConfig);
        });
    }
    
})();