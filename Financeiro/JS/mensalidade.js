document.addEventListener('DOMContentLoaded', function() {
    // Toggle do menu lateral
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.gd-sidebar');
    const mainContent = document.querySelector('.gd-main');
    
    console.log('Elementos encontrados:', {
        sidebarToggle: !!sidebarToggle,
        sidebar: !!sidebar,
        mainContent: !!mainContent
    });
    
    if (sidebarToggle && sidebar && mainContent) {
        sidebarToggle.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                // Mobile: mostrar/esconder completamente
                sidebar.classList.toggle('show');
            } else {
                // Desktop: colapsar/expandir
                sidebar.classList.toggle('collapsed');
                mainContent.classList.toggle('sidebar-collapsed');
            }
        });
    }

    // Fechar menu quando clicar fora (mobile)
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && 
            sidebar &&
            !sidebar.contains(e.target) && 
            sidebarToggle &&
            !sidebarToggle.contains(e.target) &&
            sidebar.classList.contains('show')) {
            sidebar.classList.remove('show');
        }
    });

    // Remover collapsed quando mudar para mobile
    window.addEventListener('resize', function() {
        if (sidebar && mainContent) {
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('collapsed');
                mainContent.classList.remove('sidebar-collapsed');
            } else {
                sidebar.classList.remove('show');
            }
        }
    });

    // Funcionalidade específica de pagamento (mantida do código original)
    const pagamentoCards = document.querySelectorAll('.pagamento-card');
    
    pagamentoCards.forEach(function(card) {
        card.addEventListener('click', function() {
            pagamentoCards.forEach(function(c) {
                c.classList.remove('selecionado');
            });
            this.classList.add('selecionado');
        });
    });
});