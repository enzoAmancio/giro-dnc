// =============================================
// HOME.JS - Microinterações e UX Enhancements
// =============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // =============================================
    // NAVEGAÇÃO FIXA COM SOMBRA AO ROLAR
    // =============================================
    const navbar = document.querySelector('.navback');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
            navbar.style.backdropFilter = 'blur(20px)';
            navbar.style.backgroundColor = 'rgba(0, 0, 0, 0.95)';
        } else {
            navbar.style.boxShadow = 'none';
            navbar.style.backdropFilter = 'blur(10px)';
            navbar.style.backgroundColor = '#000000';
        }
        
        lastScroll = currentScroll;
    });
    
    // =============================================
    // SMOOTH SCROLL PARA ÂNCORAS
    // =============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href.length > 1) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const offsetTop = target.offsetTop - 80;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                    
                    // Fechar menu mobile após clicar
                    const navbarCollapse = document.querySelector('.navbar-collapse');
                    if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                        const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                            toggle: true
                        });
                    }
                }
            }
        });
    });
    
    // =============================================
    // ANIMAÇÃO DE ENTRADA DOS CARDS
    // =============================================
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
   if (entry.isIntersecting) {
    setTimeout(() => {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        entry.target.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
    }, index * 100);
    observer.unobserve(entry.target);
}
        });
    }, observerOptions);
    
    // Observar cards de features
    document.querySelectorAll('.blocklist li, .revblock, .loc, .redes').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        observer.observe(card);
    });
    
    // =============================================
    // EFEITO PARALLAX SUAVE NO HERO
    // =============================================
    const heroSection = document.querySelector('.girocrew');
    if (heroSection) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallaxSpeed = 0.5;
            
            if (scrolled < window.innerHeight) {
                heroSection.style.backgroundPositionY = `${scrolled * parallaxSpeed}px`;
            }
        });
    }
    
    // =============================================
    // HOVER EFFECT NOS CARDS COM TILT SUAVE
    // =============================================
    const cards = document.querySelectorAll('.blocklist li, .revblock');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
    });
    
    // =============================================
    // CONTADOR ANIMADO (SE TIVER NÚMEROS)
    // =============================================
    function animateCounter(element, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);
        const timer = setInterval(() => {
            start += increment;
            if (start >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(start);
            }
        }, 16);
    }
    
    // =============================================
    // LOADING STATE PARA LINKS EXTERNOS
    // =============================================
    const externalLinks = document.querySelectorAll('a[target="_blank"]');
    externalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const icon = this.querySelector('i');
            if (icon) {
                icon.classList.add('fa-spin');
            }
        });
    });
    
    // =============================================
    // MELHORAR FEEDBACK VISUAL DOS BOTÕES
    // =============================================
    const buttons = document.querySelectorAll('.btn, .btn-cta');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Criar efeito ripple
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // =============================================
    // LAZY LOADING PARA IMAGENS
    // =============================================
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // =============================================
    // DESTACAR SEÇÃO ATIVA NO MENU
    // =============================================
    const sections = document.querySelectorAll('section[id], div[id]');
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
    
    // =============================================
    // PRELOAD DE IMAGENS IMPORTANTES
    // =============================================
    const criticalImages = [
        'paginas/img/girocrew.png',
        'paginas/img/Girologo.jpg'
    ];
    
    criticalImages.forEach(src => {
        const img = new Image();
        img.src = `/static/${src}`;
    });
    
    // =============================================
    // ADICIONAR CLASSE ANIMADA AOS CARDS
    // =============================================
    setTimeout(() => {
        document.querySelectorAll('.blocklist li, .revblock').forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
                card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            }, index * 100);
        });
    }, 200);
    
    console.log('🎨 Giro Dance - Home carregada com sucesso!');
});

// =============================================
// ADICIONAR ESTILO PARA EFEITO RIPPLE
// =============================================
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .btn, .btn-cta {
        position: relative;
        overflow: hidden;
    }
`;
document.head.appendChild(style);
