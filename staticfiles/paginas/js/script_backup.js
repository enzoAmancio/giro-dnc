/**
 * ========================================
 * GIRO DANCE - MENU LATERAL RESPONSIVO
 * ABORDAGEM MOBILE-FIRST
 * ========================================
 * 
 * CORREÇÕES APLICADAS:
 * ✅ Mobile-first: Menu projetado primeiro para telas pequenas
 * ✅ Menu visível e funcional em TODAS as resoluções
 * ✅ Hambúrguer acionável por qualquer ícone do header (desktop)
 * ✅ Menus acordeões fecham corretamente ao colapsar sidebar
 * ✅ Botão "Sair" sempre visível e funcional
 * ✅ Transições suaves e animações fluidas
 * ✅ Clique fora do menu fecha (mobile)
 * ✅ Comportamento consistente em todas as páginas
 * ✅ Sem bugs de estado ou atrasos em cliques
 * 
 * NÃO ALTERA: Back-end, rotas, autenticação, design visual
 */

(function() {
    'use strict';

    // ==================== CONSTANTES E CONFIGURAÇÕES ====================
    const BREAKPOINT_MOBILE = 1024; // Mobile + Tablet: menu hambúrguer até 1024px
    const TRANSITION_DURATION = 300; // ms - sincronizado com CSS
    const DEBOUNCE_DELAY = 250; // ms - para resize
    
    // ==================== ELEMENTOS DO DOM ====================
    let sidebarToggle, sidebar, mainContent, topbarIcons, accordions;
    
    // ==================== INICIALIZAÇÃO ====================
    document.addEventListener('DOMContentLoaded', init);
    
    function init() {
        // Capturar elementos
        sidebarToggle = document.getElementById('sidebar-toggle');
        sidebar = document.querySelector('.gd-sidebar');
        mainContent = document.querySelector('.gd-main');
        topbarIcons = document.querySelectorAll('.gd-topbar-content > *');
        
        // Verificar se elementos existem
        if (!sidebar) {
            console.warn('⚠️ Sidebar não encontrado nesta página');
            return;
        }
        
        console.log('✅ Menu lateral inicializado (MOBILE-FIRST):', {
            mobile: isMobile(),
            elementos: {
                toggle: !!sidebarToggle,
                sidebar: !!sidebar,
                main: !!mainContent,
                icons: topbarIcons.length
            }
        });
        
        // Configurar estado inicial
        setupInitialState();
        
        // Adicionar event listeners
        attachEventListeners();
        
        // Configurar acordeões
        setupAccordions();
        
        // Configurar calendário (se existir)
        setupCalendar();
    }
    
    // ==================== DETECÇÃO DE DISPOSITIVO ====================
    
    /**
     * Verifica se está em modo mobile
     * @returns {boolean}
     */
    function isMobile() {
        return window.innerWidth <= BREAKPOINT_MOBILE;
    }

    
    // ==================== CONFIGURAÇÃO INICIAL ====================
    
    /**
     * Configura o estado inicial do menu baseado no tamanho da tela
     * MOBILE-FIRST: Começa com menu escondido no mobile, expandido no desktop
     */
    function setupInitialState() {
        if (isMobile()) {
            // MOBILE: Menu escondido por padrão (MOBILE-FIRST)
            sidebar.classList.remove('show', 'collapsed');
            if (mainContent) {
                mainContent.classList.remove('sidebar-collapsed');
            }
        } else {
            // DESKTOP: Menu expandido por padrão
            sidebar.classList.remove('show', 'collapsed');
            if (mainContent) {
                mainContent.classList.remove('sidebar-collapsed');
            }
        }
    }
    
    // ==================== EVENT LISTENERS ====================
    
    /**
     * Adiciona todos os event listeners necessários
     */
    function attachEventListeners() {
        // 1. Botão hambúrguer principal
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', handleToggleClick);
        }
        
        // 2. CORREÇÃO: Qualquer ícone do header pode acionar o menu (apenas desktop)
        topbarIcons.forEach(icon => {
            icon.addEventListener('click', function(e) {
                // Só funciona em desktop e se não for um link
                if (!isMobile() && !e.target.closest('a')) {
                    e.stopPropagation();
                    handleToggleClick();
                }
            });
        });
        
        // 3. Clique fora do menu fecha (apenas mobile)
        document.addEventListener('click', handleOutsideClick);
        
        // 4. Resize da janela (debounced)
        let resizeTimeout;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(handleResize, DEBOUNCE_DELAY);
        });
        
        // 5. Prevenir propagação de cliques dentro do sidebar
        if (sidebar) {
            sidebar.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }
        
        // 6. CORREÇÃO: Garantir que botão "Sair" seja sempre clicável
        const logoutButtons = document.querySelectorAll('a[href*="logout"]');
        logoutButtons.forEach(btn => {
            btn.style.pointerEvents = 'auto';
            btn.style.cursor = 'pointer';
        });
    }
    
    // ==================== HANDLERS DE EVENTOS ====================
    
    /**
     * Handler para clique no botão de toggle
     */
    function handleToggleClick(e) {
        if (e) {
            e.stopPropagation();
            e.preventDefault();
        }
        
        if (isMobile()) {
            toggleMobile();
        } else {
            toggleDesktop();
        }
    }
    
    /**
     * Handler para cliques fora do menu (fecha no mobile)
     */
    function handleOutsideClick(e) {
        if (!isMobile()) return;
        
        // Se o menu está aberto e o clique foi fora dele
        if (sidebar.classList.contains('show')) {
            closeMobile();
        }
    }
    
    /**
     * Handler para resize da janela
     * Garante transição suave entre mobile e desktop
     */
    function handleResize() {
        if (isMobile()) {
            // Mudou para mobile: remover collapsed, manter show se estava aberto
            sidebar.classList.remove('collapsed');
            if (mainContent) {
                mainContent.classList.remove('sidebar-collapsed');
            }
        } else {
            // Mudou para desktop: remover show, manter expandido por padrão
            sidebar.classList.remove('show');
            sidebar.classList.remove('collapsed');
            if (mainContent) {
                mainContent.classList.remove('sidebar-collapsed');
            }
        }
    }
    
    // ==================== FUNÇÕES DE CONTROLE DO MENU ====================
    
    /**
     * MOBILE: Abre/fecha o menu deslizando da esquerda
     */
    function toggleMobile() {
        if (sidebar.classList.contains('show')) {
            closeMobile();
        } else {
            openMobile();
        }
    }
    
    /**
     * MOBILE: Abre o menu
     */
    function openMobile() {
        sidebar.classList.add('show');
        document.body.classList.add('sidebar-open');
    }
    
    /**
     * MOBILE: Fecha o menu
     */
    function closeMobile() {
        sidebar.classList.remove('show');
        document.body.classList.remove('sidebar-open');
    }
    
    /**
     * DESKTOP: Expande/colapsa o menu
     */
    function toggleDesktop() {
        if (sidebar.classList.contains('collapsed')) {
            expandDesktop();
        } else {
            collapseDesktop();
        }
    }
    
    /**
     * DESKTOP: Expande o menu
     */
    function expandDesktop() {
        sidebar.classList.remove('collapsed');
        if (mainContent) {
            mainContent.classList.remove('sidebar-collapsed');
        }
    }
    
    /**
     * DESKTOP: Colapsa o menu (ícones apenas)
     * CORREÇÃO: Fecha todos os acordeões automaticamente
     */
    function collapseDesktop() {
        sidebar.classList.add('collapsed');
        if (mainContent) {
            mainContent.classList.add('sidebar-collapsed');
        }
        
        // CORREÇÃO: Fechar todos os acordeões quando colapsa
        closeAllAccordions();
    }
    
    // ==================== GESTÃO DE ACORDEÕES ====================
    
    /**
     * Configura os acordeões do Bootstrap
     */
    function setupAccordions() {
        accordions = sidebar.querySelectorAll('.collapse');
        
        // Observar mudanças na classe .collapsed para fechar acordeões
        if (window.MutationObserver && sidebar) {
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.attributeName === 'class') {
                        const isCollapsed = sidebar.classList.contains('collapsed');
                        const isMobileView = isMobile();
                        
                        // Só fecha acordeões no desktop quando colapsa
                        if (isCollapsed && !isMobileView) {
                            closeAllAccordions();
                        }
                    }
                });
            });
            
            observer.observe(sidebar, {
                attributes: true,
                attributeFilter: ['class']
            });
        }
    }
    
    /**
     * Fecha todos os acordeões usando Bootstrap Collapse API
     * CORREÇÃO: Agora funciona corretamente com Financeiro e outros menus
     */
    function closeAllAccordions() {
        if (!accordions || accordions.length === 0) return;
        
        accordions.forEach(function(accordion) {
            // Usar Bootstrap Collapse API se disponível
            if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
                const bsCollapse = bootstrap.Collapse.getInstance(accordion);
                if (bsCollapse) {
                    bsCollapse.hide();
                } else {
                    // Se não tem instância, só remove a classe
                    accordion.classList.remove('show');
                }
            } else {
                // Fallback: remover classe manualmente
                accordion.classList.remove('show');
            }
        });
    }
    
    // ==================== CALENDÁRIO ====================
    
    function setupCalendar() {
        const prevMonth = document.getElementById('prev-month');
        const nextMonth = document.getElementById('next-month');
        const currentMonthElement = document.getElementById('current-month');
        
        if (!currentMonthElement) return; // Calendário não existe nesta página
        
        const months = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ];
        
        let currentMonthIndex = new Date().getMonth();
        let currentYear = new Date().getFullYear();
        
        function updateCalendar() {
            currentMonthElement.textContent = `${months[currentMonthIndex]} ${currentYear}`;
            generateCalendarDays();
        }
        
        function generateCalendarDays() {
            const calendarDays = document.getElementById('calendario');
            if (!calendarDays) return;
            
            const firstDay = new Date(currentYear, currentMonthIndex, 1);
            const lastDay = new Date(currentYear, currentMonthIndex + 1, 0);
            const daysInMonth = lastDay.getDate();
            const startingDayOfWeek = firstDay.getDay();
            
            let calendarHTML = `
                <div class="calendario-weekdays">
                    <span>Dom</span>
                    <span>Seg</span>
                    <span>Ter</span>
                    <span>Qua</span>
                    <span>Qui</span>
                    <span>Sex</span>
                    <span>Sáb</span>
                </div>
                <div class="calendario-days">
            `;
            
            // Dias vazios antes do início do mês
            for (let i = 0; i < startingDayOfWeek; i++) {
                calendarHTML += '<span class="calendario-day other-month"></span>';
            }
            
            // Dias do mês
            for (let day = 1; day <= daysInMonth; day++) {
                let dayClass = 'calendario-day';
                
                // Destacar dias com aulas (exemplo)
                const highlightDays = [11, 12, 18, 19, 25, 26];
                if (highlightDays.includes(day)) {
                    dayClass += ' highlight';
                }
                
                calendarHTML += `<span class="${dayClass}">${day}</span>`;
            }
            
            calendarHTML += '</div>';
            calendarDays.innerHTML = calendarHTML;
        }
        
        if (prevMonth && nextMonth) {
            prevMonth.addEventListener('click', function() {
                currentMonthIndex--;
                if (currentMonthIndex < 0) {
                    currentMonthIndex = 11;
                    currentYear--;
                }
                updateCalendar();
            });
            
            nextMonth.addEventListener('click', function() {
                currentMonthIndex++;
                if (currentMonthIndex > 11) {
                    currentMonthIndex = 0;
                    currentYear++;
                }
                updateCalendar();
            });
        }
        
        // Inicializar calendário
        updateCalendar();
    }
    
})();

