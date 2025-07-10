
// Notificação de erro específica para a tela do Gestor
// Este arquivo deve ser incluído no template gestor_view.html

(function() {
    'use strict';

    // Função principal para mostrar notificação de erro
    function showGestorErrorNotification(message, type = 'error') {
        // Remove notificações existentes
        const existingNotifications = document.querySelectorAll('.gestor-error-notification');
        existingNotifications.forEach(notification => notification.remove());

        // Cria o elemento da notificação
        const notification = document.createElement('div');
        notification.className = `gestor-error-notification ${type}`;
        
        // Define o ícone baseado no tipo
        let icon = '⚠️';
        if (type === 'error') icon = '❌';
        if (type === 'warning') icon = '⚠️';
        if (type === 'success') icon = '✅';
        
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${icon}</span>
                <span class="notification-text">${message}</span>
                <button class="notification-close" onclick="closeGestorNotification(this)" aria-label="Fechar">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        // Adiciona os estilos CSS se ainda não existirem
        if (!document.querySelector('#gestor-notification-styles')) {
            const style = document.createElement('style');
            style.id = 'gestor-notification-styles';
            style.textContent = `
                .gestor-error-notification {
                    position: fixed;
                    top: 80px; /* Abaixo da navbar */
                    right: 20px;
                    min-width: 320px;
                    max-width: 400px;
                    padding: 16px 20px;
                    border-radius: 12px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
                    z-index: 9999;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    font-size: 14px;
                    animation: slideInFromRight 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }

                .gestor-error-notification.error {
                    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
                    color: white;
                    border-left: 4px solid #ff4757;
                }

                .gestor-error-notification.warning {
                    background: linear-gradient(135deg, #ffa726 0%, #ff9800 100%);
                    color: white;
                    border-left: 4px solid #f57c00;
                }

                .gestor-error-notification.success {
                    background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%);
                    color: white;
                    border-left: 4px solid #388e3c;
                }

                .notification-content {
                    display: flex;
                    align-items: flex-start;
                    gap: 12px;
                }

                .notification-icon {
                    font-size: 18px;
                    flex-shrink: 0;
                    margin-top: 2px;
                }

                .notification-text {
                    flex: 1;
                    font-weight: 500;
                    line-height: 1.5;
                    word-wrap: break-word;
                }

                .notification-close {
                    background: none;
                    border: none;
                    color: inherit;
                    cursor: pointer;
                    padding: 4px;
                    width: 28px;
                    height: 28px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                    transition: all 0.2s ease;
                    flex-shrink: 0;
                    opacity: 0.8;
                }

                .notification-close:hover {
                    background-color: rgba(255, 255, 255, 0.2);
                    opacity: 1;
                    transform: scale(1.1);
                }

                @keyframes slideInFromRight {
                    from {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }

                @keyframes slideOutToRight {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                }

                .gestor-error-notification.closing {
                    animation: slideOutToRight 0.3s ease-in;
                }

                /* Responsividade para mobile */
                @media (max-width: 768px) {
                    .gestor-error-notification {
                        top: 70px;
                        right: 15px;
                        left: 15px;
                        min-width: auto;
                        max-width: none;
                    }
                }

                /* Ajuste para quando há múltiplas notificações */
                .gestor-error-notification:nth-child(n+2) {
                    top: calc(80px + 80px * (var(--notification-index, 0)));
                }
            `;
            document.head.appendChild(style);
        }

        // Adiciona a notificação ao body
        document.body.appendChild(notification);

        // Remove automaticamente após 7 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                closeGestorNotification(notification.querySelector('.notification-close'));
            }
        }, 7000);

        return notification;
    }

    // Função para fechar notificação
    window.closeGestorNotification = function(closeBtn) {
        const notification = closeBtn.closest('.gestor-error-notification');
        if (notification) {
            notification.classList.add('closing');
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    };

    // Função específica para erro de assinatura inválida
    function showInvalidSignatureError() {
        showGestorErrorNotification('Arquivo de assinatura inválido. Verifique se o arquivo está correto e tente novamente.', 'error');
    }

    // Função para interceptar erros do formulário de chamado
    function setupGestorFormErrorHandling() {
        const chamadoForm = document.querySelector('form.styled-form');
        
        if (chamadoForm) {
            chamadoForm.addEventListener('submit', function(e) {
                // Intercepta o submit para tratar erros via AJAX (opcional)
                // Se você quiser manter o comportamento padrão do Django, remova esta parte
                
                const formData = new FormData(chamadoForm);
                
                // Verifica se há arquivo de assinatura
                const assinaturaInput = chamadoForm.querySelector('input[type="file"][name*="assinatura"]');
                if (assinaturaInput && assinaturaInput.files.length > 0) {
                    // Aqui você pode adicionar validações do lado cliente se necessário
                    console.log('Arquivo de assinatura selecionado:', assinaturaInput.files[0].name);
                }
            });
        }
    }

    // Função para capturar mensagens de erro do Django
    function handleDjangoMessages() {
        // Procura por mensagens de erro do Django Messages Framework
        const djangoMessages = document.querySelectorAll('.alert-danger, .messages .error');
        
        djangoMessages.forEach(message => {
            const text = message.textContent.trim();
            if (text.includes('Arquivo de assinatura inválido')) {
                showInvalidSignatureError();
                message.style.display = 'none'; // Esconde a mensagem original
            } else if (text) {
                showGestorErrorNotification(text, 'error');
                message.style.display = 'none';
            }
        });
    }

    // Função para mostrar erros de validação de formulário
    function handleFormValidationErrors() {
        const errorLists = document.querySelectorAll('.errorlist');
        
        errorLists.forEach(errorList => {
            const errors = errorList.querySelectorAll('li');
            errors.forEach(error => {
                const errorText = error.textContent.trim();
                if (errorText.includes('Arquivo de assinatura inválido')) {
                    showInvalidSignatureError();
                } else if (errorText) {
                    showGestorErrorNotification(errorText, 'error');
                }
            });
            // Esconde a lista de erros original
            errorList.style.display = 'none';
        });
    }

    // Função para mostrar notificação de sucesso
    function showSuccessNotification(message) {
        showGestorErrorNotification(message, 'success');
    }

    // Inicialização quando o DOM estiver carregado
    document.addEventListener('DOMContentLoaded', function() {
        setupGestorFormErrorHandling();
        handleDjangoMessages();
        handleFormValidationErrors();
        
        // Observa mudanças no DOM para capturar novos erros
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length > 0) {
                    handleDjangoMessages();
                    handleFormValidationErrors();
                }
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });

    // Expõe funções globalmente para uso em outros scripts
    window.showGestorErrorNotification = showGestorErrorNotification;
    window.showInvalidSignatureError = showInvalidSignatureError;
    window.showGestorSuccessNotification = showSuccessNotification;

})();
