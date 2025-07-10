// Checkbox Futurista Compacto - JavaScript

class CompactFuturisticCheckbox {
    constructor(container) {
        this.container = container;
        this.checkbox = container.querySelector('input[type="checkbox"]');
        this.checkmark = container.querySelector('.compact-checkmark');
        this.particles = container.querySelector('.compact-particles');
        
        this.init();
    }
    
    init() {
        this.createParticles();
        this.addEventListeners();
        this.createSoundEffects();
    }
    
    createParticles() {
        if (!this.particles) {
            this.particles = document.createElement('div');
            this.particles.className = 'compact-particles';
            this.container.appendChild(this.particles);
        }
        
        // Criar partículas iniciais (menos que o original)
        for (let i = 0; i < 3; i++) {
            this.createParticle();
        }
    }
    
    createParticle() {
        const particle = document.createElement('div');
        particle.className = 'compact-particle';
        
        // Posição aleatória
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 2 + 's';
        particle.style.animationDuration = (1.5 + Math.random() * 1) + 's';
        
        this.particles.appendChild(particle);
        
        // Remover partícula após animação
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 3000);
    }
    
    addEventListeners() {
        // Hover effects
        this.container.addEventListener('mouseenter', () => {
            this.onHover();
        });
        
        this.container.addEventListener('mouseleave', () => {
            this.onLeave();
        });
        
        // Click effects
        this.checkbox.addEventListener('change', (e) => {
            this.onChange(e.target.checked);
        });
        
        // Efeito de clique visual mais sutil
        this.container.addEventListener('mousedown', () => {
            this.container.style.transform = 'translateY(0px) scale(0.98)';
        });
        
        this.container.addEventListener('mouseup', () => {
            this.container.style.transform = 'translateY(-1px) scale(1)';
        });
    }
    
    onHover() {
        // Criar menos partículas no hover
        for (let i = 0; i < 2; i++) {
            setTimeout(() => this.createParticle(), i * 50);
        }
        
        // Efeito de vibração mais sutil
        this.checkmark.style.animation = 'compact-subtle-vibrate 0.2s ease-in-out';
        setTimeout(() => {
            this.checkmark.style.animation = '';
        }, 200);
        
        // Som de hover (se disponível)
        this.playSound('hover');
    }
    
    onLeave() {
        // Parar efeitos de hover
    }
    
    onChange(isChecked) {
        if (isChecked) {
            this.onCheck();
        } else {
            this.onUncheck();
        }
    }
    
    onCheck() {
        // Explosão de partículas mais sutil
        this.createCompactParticleExplosion();
        
        // Efeito de onda mais sutil
        this.createCompactRippleEffect();
        
        // Som de confirmação
        this.playSound('check');
        
        // Vibração mais sutil (se suportado)
        if (navigator.vibrate) {
            navigator.vibrate([30, 20, 30]);
        }
        
        // Animação de sucesso mais sutil
        this.animateCompactSuccess();
    }
    
    onUncheck() {
        // Som de desmarcar
        this.playSound('uncheck');
        
        // Efeito de fade das partículas
        this.fadeParticles();
    }
    
    createCompactParticleExplosion() {
        const colors = ['var(--primary-color)', 'var(--accent-color)', 'var(--highlight-color)'];
        
        // Menos partículas para o design compacto
        for (let i = 0; i < 6; i++) {
            const particle = document.createElement('div');
            particle.className = 'compact-explosion-particle';
            particle.style.position = 'absolute';
            particle.style.width = '2px';
            particle.style.height = '2px';
            particle.style.borderRadius = '50%';
            particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            particle.style.left = '50%';
            particle.style.top = '50%';
            particle.style.pointerEvents = 'none';
            particle.style.zIndex = '1000';
            
            const angle = (i / 6) * Math.PI * 2;
            const distance = 15 + Math.random() * 10; // Distância menor
            const duration = 0.4 + Math.random() * 0.2; // Duração menor
            
            particle.style.animation = `compact-explode-${i} ${duration}s ease-out forwards`;
            
            // Criar keyframes dinâmicos
            const keyframes = `
                @keyframes compact-explode-${i} {
                    0% {
                        transform: translate(-50%, -50%) scale(1);
                        opacity: 1;
                    }
                    100% {
                        transform: translate(calc(-50% + ${Math.cos(angle) * distance}px), calc(-50% + ${Math.sin(angle) * distance}px)) scale(0);
                        opacity: 0;
                    }
                }
            `;
            
            const style = document.createElement('style');
            style.textContent = keyframes;
            document.head.appendChild(style);
            
            this.checkmark.appendChild(particle);
            
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.parentNode.removeChild(particle);
                }
                document.head.removeChild(style);
            }, duration * 1000);
        }
    }
    
    createCompactRippleEffect() {
        const ripple = document.createElement('div');
        ripple.style.position = 'absolute';
        ripple.style.left = '50%';
        ripple.style.top = '50%';
        ripple.style.width = '0';
        ripple.style.height = '0';
        ripple.style.borderRadius = '50%';
        ripple.style.border = '1px solid var(--highlight-color)';
        ripple.style.transform = 'translate(-50%, -50%)';
        ripple.style.animation = 'compact-ripple-expand 0.4s ease-out forwards';
        ripple.style.pointerEvents = 'none';
        
        this.container.appendChild(ripple);
        
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 400);
    }
    
    animateCompactSuccess() {
        // Animação de pulso mais sutil
        this.container.style.animation = 'compact-success-pulse 0.5s ease-in-out';
        setTimeout(() => {
            this.container.style.animation = '';
        }, 500);
    }
    
    fadeParticles() {
        const particles = this.particles.querySelectorAll('.compact-particle');
        particles.forEach(particle => {
            particle.style.opacity = '0';
            particle.style.transition = 'opacity 0.2s ease';
        });
    }
    
    createSoundEffects() {
        // Criar contexto de áudio para efeitos sonoros mais sutis
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.sounds = {
                hover: this.createTone(600, 0.05, 0.03),
                check: this.createTone(900, 0.15, 0.05),
                uncheck: this.createTone(400, 0.1, 0.04)
            };
        } catch (e) {
            console.log('Audio context not supported');
        }
    }
    
    createTone(frequency, duration, volume = 0.05) {
        if (!this.audioContext) return null;
        
        return () => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);
            oscillator.type = 'sine';
            
            gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(volume, this.audioContext.currentTime + 0.01);
            gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + duration);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + duration);
        };
    }
    
    playSound(type) {
        if (this.sounds && this.sounds[type]) {
            this.sounds[type]();
        }
    }
}

// CSS adicional para animações JavaScript compactas
const compactAdditionalCSS = `
@keyframes compact-subtle-vibrate {
    0%, 100% { transform: translateX(0); }
    50% { transform: translateX(0.5px); }
}

@keyframes compact-ripple-expand {
    0% {
        width: 0;
        height: 0;
        opacity: 1;
    }
    100% {
        width: 40px;
        height: 40px;
        opacity: 0;
    }
}

@keyframes compact-success-pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}
`;

// Adicionar CSS adicional
const compactStyle = document.createElement('style');
compactStyle.textContent = compactAdditionalCSS;
document.head.appendChild(compactStyle);

// Inicialização automática para checkboxes compactos
document.addEventListener('DOMContentLoaded', function() {
    const compactCheckboxContainers = document.querySelectorAll('.compact-checkbox-container');
    compactCheckboxContainers.forEach(container => {
        if (!container.dataset.compactInitialized) {
            new CompactFuturisticCheckbox(container);
            container.dataset.compactInitialized = 'true';
        }
    });
});

// Exportar para uso em módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CompactFuturisticCheckbox;
}