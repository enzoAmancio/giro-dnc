document.addEventListener('DOMContentLoaded', function() {
  var btnMenu = document.getElementById('sidebar-toggle');
  var sidebar = document.querySelector('.gd-sidebar');
  if (btnMenu && sidebar) {
    btnMenu.addEventListener('click', function() {
      sidebar.classList.toggle('sidebar-collapsed');
      // Esconde as palavras das opções
      document.querySelectorAll('.sidebar-text, .gd-submenu .sidebar-text, .gd-submenu span').forEach(function(el) {
        if (sidebar.classList.contains('sidebar-collapsed')) {
          el.style.display = 'none';
        } else {
          el.style.display = '';
        }
      });
      // Fecha todos os submenus abertos ao recolher a sidebar
      if (sidebar.classList.contains('sidebar-collapsed')) {
        document.querySelectorAll('.collapse.show').forEach(function(submenu) {
          submenu.classList.remove('show');
        });
      }
    });
  }
});
document.addEventListener('DOMContentLoaded', function() {
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