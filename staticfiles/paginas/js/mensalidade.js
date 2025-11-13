document.addEventListener('DOMContentLoaded', function() {

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
                sidebar.classList.toggle('show');
            } else {
                sidebar.classList.toggle('collapsed');
                mainContent.classList.toggle('sidebar-collapsed');
            }
        });
    }


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