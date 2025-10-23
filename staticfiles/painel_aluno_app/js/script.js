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
            !sidebar.contains(e.target) && 
            !sidebarToggle.contains(e.target) &&
            sidebar.classList.contains('show')) {
            sidebar.classList.remove('show');
        }
    });

    // Remover collapsed quando mudar para mobile
    window.addEventListener('resize', function() {
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('collapsed');
            mainContent.classList.remove('sidebar-collapsed');
        } else {
            sidebar.classList.remove('show');
        }
    });

    // Funcionalidade do calendário
    const prevMonth = document.getElementById('prev-month');
    const nextMonth = document.getElementById('next-month');
    const currentMonthElement = document.getElementById('current-month');
    
    const months = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ];
    
    let currentMonthIndex = 9; // Outubro (índice 9)
    let currentYear = 2025;
    
    function updateCalendar() {
        if (currentMonthElement) {
            currentMonthElement.textContent = `${months[currentMonthIndex]} ${currentYear}`;
        }
        generateCalendarDays();
    }
    
    function generateCalendarDays() {
        const calendarDays = document.getElementById('calendario');
        if (!calendarDays) return;
        
        const firstDay = new Date(currentYear, currentMonthIndex, 1);
        const lastDay = new Date(currentYear, currentMonthIndex + 1, 0);
        const daysInMonth = lastDay.getDate();
        const startingDayOfWeek = firstDay.getDay();
        
        // Criar estrutura do calendário
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
        
        // Adicionar dias vazios para começar no dia correto da semana
        for (let i = 0; i < startingDayOfWeek; i++) {
            calendarHTML += '<span class="calendario-day other-month"></span>';
        }
        
        // Adicionar os dias do mês
        for (let day = 1; day <= daysInMonth; day++) {
            let dayClass = 'calendario-day';
            
            // Destacar alguns dias como exemplo (dias com aulas)
            const highlightDays = [11, 12, 18, 19, 25, 26]; // Sextas e sábados
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
    
    // Inicializar o calendário
    updateCalendar();
});