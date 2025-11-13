// =============================================
// SISTEMA.JS - JavaScript para página "Conheça nosso Sistema"
// =============================================

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar AOS (Animate On Scroll)
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true,
        offset: 100
    });

    // =============================================
    // CTA FLUTUANTE - Mostrar/Ocultar ao rolar
    // =============================================
    const floatingCta = document.getElementById('floatingCta');
    let lastScrollTop = 0;

    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Mostrar CTA após rolar 300px
        if (scrollTop > 300) {
            floatingCta.classList.add('show');
        } else {
            floatingCta.classList.remove('show');
        }
        
        lastScrollTop = scrollTop;
    });

    // =============================================
    // SMOOTH SCROLL para links âncora
    // =============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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
                }
            }
        });
    });

    // =============================================
    // VALIDAÇÃO E ENVIO DO FORMULÁRIO DE CONTATO
    // =============================================
    const contatoForm = document.getElementById('contatoForm');
    const successMessage = document.getElementById('successMessage');
    const errorMessage = document.getElementById('errorMessage');

    if (contatoForm) {
        contatoForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Limpar mensagens anteriores
            successMessage.classList.remove('show');
            errorMessage.classList.remove('show');
            clearErrors();

            // Validar formulário
            if (!validateForm()) {
                return;
            }

            // Coletar dados do formulário
            const formData = {
                nome: document.getElementById('nome').value.trim(),
                email: document.getElementById('email').value.trim(),
                telefone: document.getElementById('telefone').value.trim(),
                empresa: document.getElementById('empresa').value.trim(),
                mensagem: document.getElementById('mensagem').value.trim()
            };

            // Desabilitar botão durante o envio
            const submitBtn = contatoForm.querySelector('.btn-submit');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Enviando...</span>';

            try {
                // Obter CSRF token
                const csrftoken = getCookie('csrftoken');

                // Enviar para o backend Django
                const response = await fetch('/api/contato-consultor/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify(formData)
                });

                if (response.ok) {
                    // Sucesso
                    successMessage.classList.add('show');
                    contatoForm.reset();
                    
                    // Rolar até a mensagem de sucesso
                    setTimeout(() => {
                        successMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }, 100);

                    // Ocultar mensagem após 8 segundos
                    setTimeout(() => {
                        successMessage.classList.remove('show');
                    }, 8000);
                } else {
                    // Erro
                    errorMessage.classList.add('show');
                    setTimeout(() => {
                        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }, 100);
                }
            } catch (error) {
                console.error('Erro ao enviar formulário:', error);
                errorMessage.classList.add('show');
                setTimeout(() => {
                    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }, 100);
            } finally {
                // Reabilitar botão
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        });
    }

    // =============================================
    // FUNÇÕES DE VALIDAÇÃO
    // =============================================
    function validateForm() {
        let isValid = true;

        // Validar nome
        const nome = document.getElementById('nome');
        if (nome.value.trim().length < 3) {
            showError(nome, 'Nome deve ter no mínimo 3 caracteres');
            isValid = false;
        }

        // Validar email
        const email = document.getElementById('email');
        if (!isValidEmail(email.value.trim())) {
            showError(email, 'Email inválido');
            isValid = false;
        }

        // Validar telefone
        const telefone = document.getElementById('telefone');
        if (!isValidPhone(telefone.value.trim())) {
            showError(telefone, 'Telefone inválido');
            isValid = false;
        }

        // Validar mensagem
        const mensagem = document.getElementById('mensagem');
        if (mensagem.value.trim().length < 10) {
            showError(mensagem, 'Mensagem deve ter no mínimo 10 caracteres');
            isValid = false;
        }

        return isValid;
    }

    function showError(input, message) {
        const formGroup = input.closest('.form-group');
        formGroup.classList.add('error');
        const errorSpan = formGroup.querySelector('.error-message');
        if (errorSpan) {
            errorSpan.textContent = message;
        }
    }

    function clearErrors() {
        document.querySelectorAll('.form-group.error').forEach(group => {
            group.classList.remove('error');
        });
    }

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function isValidPhone(phone) {
        // Remove caracteres não numéricos
        const cleaned = phone.replace(/\D/g, '');
        // Verifica se tem entre 10 e 11 dígitos
        return cleaned.length >= 10 && cleaned.length <= 11;
    }

    // Limpar erro ao digitar
    document.querySelectorAll('.form-group input, .form-group textarea').forEach(input => {
        input.addEventListener('input', function() {
            this.closest('.form-group').classList.remove('error');
        });
    });

    // =============================================
    // MÁSCARAS DE INPUT
    // =============================================
    const telefoneInput = document.getElementById('telefone');
    if (telefoneInput) {
        telefoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length <= 11) {
                if (value.length <= 10) {
                    // (99) 9999-9999
                    value = value.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
                } else {
                    // (99) 99999-9999
                    value = value.replace(/^(\d{2})(\d{5})(\d{0,4}).*/, '($1) $2-$3');
                }
            }
            
            e.target.value = value;
        });
    }

    // =============================================
    // FUNÇÕES DOS BOTÕES DE PLANOS
    // =============================================
    window.iniciarTeste = function(plano) {
        // Simular modal ou redirecionar para página de teste
        const planoNomes = {
            'basico': 'Básico',
            'intermediario': 'Intermediário',
            'pro': 'Pro'
        };

        if (confirm(`Deseja iniciar o teste gratuito de 7 dias do plano ${planoNomes[plano]}?\n\nVocê será redirecionado para a página de cadastro.`)) {
            // Aqui você pode redirecionar para uma página de registro
            // ou abrir um modal de cadastro
            console.log(`Iniciar teste do plano: ${plano}`);
            
            // Exemplo: redirecionar com parâmetro
            // window.location.href = `/cadastro/?plano=${plano}&teste=true`;
            
            // Por enquanto, rolar até o formulário de contato
            document.getElementById('contato').scrollIntoView({ behavior: 'smooth' });
        }
    };

    window.assinarPlano = function(plano) {
        const planoNomes = {
            'basico': 'Básico',
            'intermediario': 'Intermediário',
            'pro': 'Pro'
        };

        const planoPrecos = {
            'basico': 'R$ 97',
            'intermediario': 'R$ 197',
            'pro': 'R$ 397'
        };

        if (confirm(`Deseja assinar o plano ${planoNomes[plano]} por ${planoPrecos[plano]}/mês?\n\nVocê será redirecionado para a página de pagamento.`)) {
            console.log(`Assinar plano: ${plano}`);
            
            // Exemplo: redirecionar para página de checkout
            // window.location.href = `/checkout/?plano=${plano}`;
            
            // Por enquanto, rolar até o formulário de contato
            document.getElementById('contato').scrollIntoView({ behavior: 'smooth' });
        }
    };

    // =============================================
    // FUNÇÃO PARA OBTER CSRF TOKEN
    // =============================================
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // =============================================
    // EFEITOS DE PARALLAX SUAVE NO HERO
    // =============================================
    const heroSection = document.querySelector('.hero-sistema');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const parallax = heroSection.querySelector('.hero-overlay');
            if (parallax && scrolled < window.innerHeight) {
                parallax.style.transform = `translateY(${scrolled * 0.5}px)`;
            }
        });
    }

    // =============================================
    // CONTADOR ANIMADO (se necessário no futuro)
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
    // OBSERVADOR DE INTERSEÇÃO para animações
    // =============================================
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observar cards e elementos animáveis
    document.querySelectorAll('.feature-card, .plano-card, .depoimento-card').forEach(el => {
        observer.observe(el);
    });

    // =============================================
    // EASTER EGG - Efeito especial ao clicar na logo
    // =============================================
    let clickCount = 0;
    const logo = document.querySelector('.navbar-brand .logo');
    if (logo) {
        logo.addEventListener('click', function() {
            clickCount++;
            if (clickCount === 5) {
                // Efeito confetti ou mensagem especial
                console.log('🎉 Você descobriu o Easter Egg! Entre em contato e ganhe um desconto especial!');
                clickCount = 0;
            }
        });
    }

    console.log('Sistema Giro - Página carregada com sucesso! 🚀');
});

// =============================================
// PREVENÇÃO DE SPAM NO FORMULÁRIO
// =============================================
let lastSubmitTime = 0;
const SUBMIT_COOLDOWN = 5000; // 5 segundos

document.addEventListener('submit', function(e) {
    const now = Date.now();
    if (now - lastSubmitTime < SUBMIT_COOLDOWN) {
        e.preventDefault();
        alert('Por favor, aguarde alguns segundos antes de enviar novamente.');
        return false;
    }
    lastSubmitTime = now;
});
