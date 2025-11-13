/**
 * ========================================
 * GIRO DANCE - MENU LATERAL RESPONSIVO
 * ========================================
 */
(function() {
    'use strict';

    let sidebarToggle, sidebar, mainContent, menuButton;

    document.addEventListener('DOMContentLoaded', init);

    function init() {
        sidebarToggle = document.getElementById('sidebar-toggle');
        sidebar = document.querySelector('.gd-sidebar');
        mainContent = document.querySelector('.gd-main');
        menuButton = document.querySelector('.sidebar-item');

        if (!sidebar || !sidebarToggle) {
            console.warn('⚠️ Elementos do menu não encontrados');
            return;
        }

        console.log('✅ Menu lateral inicializado');

        // Adiciona listener ao botão sanduíche
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleMenu();
        });

        // Fecha menu mobile se clicar fora
        document.addEventListener('click', function(e) {
            const isMobile = window.innerWidth <= 1024;
            
            if (isMobile && sidebar.classList.contains('show')) {
                // Verifica se clicou fora do sidebar e do botão
                if (!sidebar.contains(e.target) && 
                    !sidebarToggle.contains(e.target) && 
                    !menuButton.contains(e.target)) {
                    closeMobileMenu();
                }
            }
        });

        // Fecha automaticamente ao redimensionar
        window.addEventListener('resize', handleResize);
        
        // Limpa estados ao carregar
        cleanupStates();
    }

    function toggleMenu() {
        const isMobile = window.innerWidth <= 1024;

        if (isMobile) {
            // MOBILE: abre/fecha menu overlay
            const isOpen = sidebar.classList.contains('show');
            
            if (isOpen) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
            
            console.log('📱 Menu mobile:', sidebar.classList.contains('show') ? 'aberto' : 'fechado');
        } else {
            // DESKTOP: colapsa sidebar
            const isCollapsed = sidebar.classList.contains('collapsed');
            
            if (isCollapsed) {
                expandDesktopMenu();
            } else {
                collapseDesktopMenu();
            }
            
            console.log('💻 Menu desktop:', sidebar.classList.contains('collapsed') ? 'colapsado' : 'expandido');
        }
    }

    function openMobileMenu() {
        sidebar.classList.add('show');
        document.body.classList.add('menu-open');
    }

    function closeMobileMenu() {
        sidebar.classList.remove('show');
        document.body.classList.remove('menu-open');
    }

    function collapseDesktopMenu() {
        sidebar.classList.add('collapsed');
        document.body.classList.add('sidebar-collapsed');
        if (mainContent) {
            mainContent.classList.add('sidebar-collapsed');
        }
    }

    function expandDesktopMenu() {
        sidebar.classList.remove('collapsed');
        document.body.classList.remove('sidebar-collapsed');
        if (mainContent) {
            mainContent.classList.remove('sidebar-collapsed');
        }
    }

    function handleResize() {
        const isMobile = window.innerWidth <= 1024;

        if (!isMobile) {
            // Ao voltar pro desktop, remove estado mobile
            closeMobileMenu();
        } else {
            // Ao ir pro mobile, remove estado desktop
            sidebar.classList.remove('collapsed');
            document.body.classList.remove('sidebar-collapsed');
            if (mainContent) {
                mainContent.classList.remove('sidebar-collapsed');
            }
        }
    }

    function cleanupStates() {
        const isMobile = window.innerWidth <= 1024;
        
        if (isMobile) {
            // Mobile: garante que não tem classes de desktop
            sidebar.classList.remove('collapsed');
            document.body.classList.remove('sidebar-collapsed');
            if (mainContent) {
                mainContent.classList.remove('sidebar-collapsed');
            }
            // E garante que menu está fechado
            closeMobileMenu();
        } else {
            // Desktop: garante que não tem classes de mobile
            closeMobileMenu();
        }
    }

})();
