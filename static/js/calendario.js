document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var citasData = JSON.parse(document.getElementById('citas-data').textContent);
    var isSuperuser = document.getElementById('is-superuser').textContent === 'True';

    var calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'es',  // Configura el idioma a español
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        buttonText: {
            today: 'Hoy',
            month: 'Mes',
            week: 'Semana',
            day: 'Día'
        },
        events: citasData.map(function(cita) {
            return {
                title: isSuperuser ? cita.paciente + ': ' + cita.motivo : cita.motivo,
                start: cita.start,
                end: cita.end,
                backgroundColor: 'blue',
                borderColor: 'darkblue',
                textColor: 'white'
            };
        }),
        // Puedes añadir más opciones aquí si es necesario
    });

    calendar.render();
});