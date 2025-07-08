// Checkbox Futurista - JavaScript Avançado

class FuturisticCheckbox {
    constructor(container) {
        this.container = container;
        this.checkbox = container.querySelector("input[type=\"checkbox\"]");
        this.checkmark = container.querySelector(".futuristic-checkmark");
        this.particles = container.querySelector(".particles");
        
        this.init();
    }
    
    init() {
        this.createParticles();
        this.addEventListeners();
        this.createSoundEffects();
    }
    
    createParticles() {
        if (!this.particles) {
            this.particles = document.createElement("div");
            this.particles.className = "particles";
            this.container.appendChild(this.particles);
        }
        
        // Criar partículas iniciais
        for (let i = 0; i < 5; i++) {
            this.createParticle();
        }
    }
    
    createParticle() {
        const particle = document.createElement("div");
        particle.className = "particle";
        
        // Posição aleatória
        particle.style.left = Math.random() * 100 + "%";
        particle.style.animationDelay = Math.random() * 3 + "s";
        particle.style.animationDuration = (2 + Math.random() * 2) + "s";
        
        this.particles.appendChild(particle);
        
        // Remover partícula após animação
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 5000);
    }
    
    addEventListeners() {
        // Hover effects
        this.container.addEventListener("mouseenter", () => {
            this.onHover();
        });
        
        this.container.addEventListener("mouseleave", () => {
            this.onLeave();
        });
        
        // Click effects
        this.checkbox.addEventListener("change", (e) => {
            this.onChange(e.target.checked);
        });
        
        // Efeito de clique visual
        this.container.addEventListener("mousedown", () => {
            this.container.style.transform = "translateY(-1px) scale(0.98)";
        });
        
        this.container.addEventListener("mouseup", () => {
            this.container.style.transform = "translateY(-2px) scale(1)";
        });
    }
    
    onHover() {
        // Criar mais partículas no hover
        for (let i = 0; i < 3; i++) {
            setTimeout(() => this.createParticle(), i * 100);
        }
        
        // Efeito de vibração sutil
        this.checkmark.style.animation = "subtle-vibrate 0.3s ease-in-out";
        setTimeout(() => {
            this.checkmark.style.animation = "";
        }, 300);
        
        // Som de hover (se disponível)
        this.playSound("hover");
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
        // Explosão de partículas
        this.createParticleExplosion();
        
        // Efeito de onda
        this.createRippleEffect();
        
        // Som de confirmação
        this.playSound("check");
        
        // Vibração (se suportado)
        if (navigator.vibrate) {
            navigator.vibrate([50, 30, 50]);
        }
        
        // Animação de sucesso
        this.animateSuccess();
    }
    
    onUncheck() {
        // Som de desmarcar
        this.playSound("uncheck");
        
        // Efeito de fade das partículas
        this.fadeParticles();
    }
    
    createParticleExplosion() {
        const colors = ["var(--primary-color)", "var(--accent-color)", "var(--highlight-color)", "var(--text-on-primary)"];
        
        for (let i = 0; i < 12; i++) {
            const particle = document.createElement("div");
            particle.className = "explosion-particle";
            particle.style.position = "absolute";
            particle.style.width = "4px";
            particle.style.height = "4px";
            particle.style.borderRadius = "50%";
            particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            particle.style.left = "50%";
            particle.style.top = "50%";
            particle.style.pointerEvents = "none";
            particle.style.zIndex = "1000";
            
            const angle = (i / 12) * Math.PI * 2;
            const distance = 30 + Math.random() * 20;
            const duration = 0.6 + Math.random() * 0.4;
            
            particle.style.animation = `explode-${i} ${duration}s ease-out forwards`;
            
            // Criar keyframes dinâmicos
            const keyframes = `
                @keyframes explode-${i} {
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
            
            const style = document.createElement("style");
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
    
    createRippleEffect() {
        const ripple = document.createElement("div");
        ripple.style.position = "absolute";
        ripple.style.left = "50%";
        ripple.style.top = "50%";
        ripple.style.width = "0";
        ripple.style.height = "0";
        ripple.style.borderRadius = "50%";
        ripple.style.border = "2px solid var(--highlight-color)";
        ripple.style.transform = "translate(-50%, -50%)";
        ripple.style.animation = "ripple-expand 0.6s ease-out forwards";
        ripple.style.pointerEvents = "none";
        
        this.container.appendChild(ripple);
        
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 600);
    }
    
    animateSuccess() {
        // Animação de pulso de sucesso
        this.container.style.animation = "success-pulse 0.8s ease-in-out";
        setTimeout(() => {
            this.container.style.animation = "";
        }, 800);
    }
    
    fadeParticles() {
        const particles = this.particles.querySelectorAll(".particle");
        particles.forEach(particle => {
            particle.style.opacity = "0";
            particle.style.transition = "opacity 0.3s ease";
        });
    }
    
    createSoundEffects() {
        // Criar contexto de áudio para efeitos sonoros
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.sounds = {
                hover: this.createTone(800, 0.1, 0.05),
                check: this.createTone(1200, 0.2, 0.1),
                uncheck: this.createTone(600, 0.15, 0.08)
            };
        } catch (e) {
            console.log("Audio context not supported");
        }
    }
    
    createTone(frequency, duration, volume = 0.1) {
        if (!this.audioContext) return null;
        
        return () => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);
            oscillator.type = "sine";
            
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

// CSS adicional para animações JavaScript
const additionalCSS = `
@keyframes subtle-vibrate {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-1px); }
    75% { transform: translateX(1px); }
}

@keyframes ripple-expand {
    0% {
        width: 0;
        height: 0;
        opacity: 1;
    }
    100% {
        width: 100px;
        height: 100px;
        opacity: 0;
    }
}

@keyframes success-pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
`;

// Adicionar CSS adicional
const style = document.createElement("style");
style.textContent = additionalCSS;
document.head.appendChild(style);

// Inicialização automática
document.addEventListener("DOMContentLoaded", function() {
    const checkboxContainers = document.querySelectorAll(".futuristic-checkbox-container");
    checkboxContainers.forEach(container => {
        new FuturisticCheckbox(container);
    });
});

// Exportar para uso em módulos
if (typeof module !== "undefined" && module.exports) {
    module.exports = FuturisticCheckbox;
}