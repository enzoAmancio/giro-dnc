document.addEventListener('DOMContentLoaded', function() {
  const btnMenu = document.getElementById('sidebar-toggle');
  const sidebar = document.querySelector('.gd-sidebar');

  if (btnMenu && sidebar) {
    btnMenu.addEventListener('click', function() {
      sidebar.classList.toggle('sidebar-collapsed');

      
      document.querySelectorAll('.gd-submenu span').forEach(function(el) {
        el.style.display = sidebar.classList.contains('sidebar-collapsed') ? 'none' : '';
      });

      
      if (sidebar.classList.contains('sidebar-collapsed')) {
        document.querySelectorAll('.collapse.show').forEach(function(submenu) {
          submenu.classList.remove('show');
        });
      }
    });
  }

  
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