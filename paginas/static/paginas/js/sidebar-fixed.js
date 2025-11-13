document.addEventListener('DOMContentLoaded', function() {
  const btnMenu = document.getElementById('sidebar-toggle');
  const sidebar = document.querySelector('.gd-sidebar');
  
  if (btnMenu && sidebar) {
    btnMenu.addEventListener('click', function() {
      // Toggle da classe collapsed
      sidebar.classList.toggle('sidebar-collapsed');
      
      // Seleciona todos os spans dentro das opções do sidebar
      const textos = sidebar.querySelectorAll('.nav-link span, .btn-toggle span, .sidebar-option span');
      
      if (sidebar.classList.contains('sidebar-collapsed')) {
        // Quando colapsar: esconde os textos mas mantém os ícones
        textos.forEach(function(el) {
          el.style.opacity = '0';
          el.style.width = '0';
          el.style.overflow = 'hidden';
        });
        
        // Reduz largura do sidebar
        sidebar.style.width = '70px';
        
        // Fecha todos os submenus
        sidebar.querySelectorAll('.collapse.show').forEach(function(submenu) {
          submenu.classList.remove('show');
        });
        
        // Esconde os chevrons
        sidebar.querySelectorAll('.bi-chevron-down').forEach(function(chevron) {
          chevron.style.display = 'none';
        });
      } else {
        // Quando expandir: mostra os textos
        textos.forEach(function(el) {
          el.style.opacity = '1';
          el.style.width = 'auto';
          el.style.overflow = 'visible';
        });
        
        // Restaura largura do sidebar
        sidebar.style.width = '';
        
        // Mostra os chevrons
        sidebar.querySelectorAll('.bi-chevron-down').forEach(function(chevron) {
          chevron.style.display = '';
        });
      }
    });
  }

  // Mantém o highlight da opção ativa
  document.querySelectorAll('.collapse .sidebar-option').forEach(function(opt) {
    opt.addEventListener('click', function(e) {
      document.querySelectorAll('.collapse .sidebar-option').forEach(function(o) {
        o.classList.remove('sidebar-placeholder');
      });
      this.classList.add('sidebar-placeholder');
      e.stopPropagation();
    });
  });
});
