// Fortsetzung der widget.js Datei

                            <div style="width: 8px; height: 8px; background: #9ca3af; border-radius: 50%; animation: bounce 1.4s infinite 0.4s;"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(typingElement);
        
        // Add CSS animation if not already added
        if (!document.getElementById('ki-concierge-styles')) {
            const style = document.createElement('style');
            style.id = 'ki-concierge-styles';
            style.textContent = `
                @keyframes bounce {
                    0%, 60%, 100% { transform: translateY(0); }
                    30% { transform: translateY(-4px); }
                }
                
                .ki-message {
                    margin-bottom: 16px;
                    animation: fadeIn 0.3s ease;
                }
                
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                
                #ki-concierge-messages::-webkit-scrollbar {
                    width: 6px;
                }
                
                #ki-concierge-messages::-webkit-scrollbar-track {
                    background: #f1f1f1;
                    border-radius: 3px;
                }
                
                #ki-concierge-messages::-webkit-scrollbar-thumb {
                    background: #c1c1c1;
                    border-radius: 3px;
                }
                
                #ki-concierge-messages::-webkit-scrollbar-thumb:hover {
                    background: #a1a1a1;
                }
            `;
            document.head.appendChild(style);
        }
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // Remove typing indicator
    function removeTypingIndicator() {
        const typingElement = document.getElementById('ki-typing-indicator');
        if (typingElement) {
            typingElement.remove();
        }
    }
    
    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Initialize widget
    function init() {
        // Check if already initialized
        if (document.getElementById('ki-concierge-container')) {
            console.warn('KI-CONCIERGE: Widget already initialized');
            return;
        }
        
        // Load configuration
        if (!loadConfig()) {
            return;
        }
        
        // Create widget
        createWidget();
        
        console.log('KI-CONCIERGE: Widget initialized successfully');
    }
    
    // Public API
    window.KIConcierge = {
        init: init,
        open: toggleChat,
        close: toggleChat,
        sendMessage: (message) => {
            const input = document.querySelector('#ki-concierge-chat input');
            if (input) {
                input.value = message;
                sendMessage(input);
            }
        },
        updateConfig: (newConfig) => {
            config = { ...config, ...newConfig };
            // Reinitialize with new config
            const container = document.getElementById('ki-concierge-container');
            if (container) {
                container.remove();
            }
            createWidget();
        }
    };
    
    // Auto-initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();