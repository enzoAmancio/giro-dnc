/**
 * ========================================
 * GIRO DANCE - MENU LATERAL SIMPLIFICADO
 * ========================================
 */

(function() {
    'use strict';

    // ==================== ELEMENTOS DO DOM ====================
    let sidebarToggle, sidebar, mainContent;
    
    // ==================== INICIALIZAÇÃO ====================
    document.addEventListener('DOMContentLoaded', init);
    
    function init() {
        // Capturar elementos
        sidebarToggle = document.getElementById('sidebar-toggle');
        sidebar = document.querySelector('.gd-sidebar');
        mainContent = document.querySelector('.gd-main');
        
        if (!sidebar || !sidebarToggle) {
            console.warn('⚠️ Elementos do menu não encontrados');
            return;
        }
        
        console.log('✅ Menu lateral inicializado');
        
        // Event listeners
        sidebarToggle.addEventListener('click', toggleMenu);
        
        // Garantir que acordeões fechem ao colapsar
        const collapseElements = sidebar.querySelectorAll('.collapse');
        sidebar.addEventListener('transitionend', function() {
            if (sidebar.classList.contains('collapsed')) {
                collapseElements.forEach(el => {
                    const bsCollapse = bootstrap.Collapse.getInstance(el);
                    if (bsCollapse) {
                        bsCollapse.hide();
                    }
                });
            }
        });
    }
    
    // ==================== TOGGLE DO MENU ====================
    function toggleMenu(e) {
        e.preventDefault();
        
        // Simplesmente alterna entre expandido e colapsado
        sidebar.classList.toggle('collapsed');
        
        if (mainContent) {
            mainContent.classList.toggle('sidebar-collapsed');
        }
        
        console.log('Menu toggled:', sidebar.classList.contains('collapsed') ? 'colapsado' : 'expandido');
    }
    
})();
