document.addEventListener('DOMContentLoaded', function() {
    const fechaInput = document.getElementById('fecha');
    const horaContainer = document.getElementById('hora');

    flatpickr(fechaInput, {
        dateFormat: "Y-m-d",
        minDate: "today",
        inline: true,
        static: true,
        onChange: function(selectedDates, dateStr, instance) {
            // Cuando se selecciona una fecha, obtén las horas disponibles
            fetch(`/get-horas-disponibles/?fecha=${dateStr}`)
                .then(response => response.json())
                .then(horas => {
                    // Limpia las opciones actuales
                    horaContainer.innerHTML = '';
                    // Añade las nuevas opciones
                    horas.forEach(hora => {
                        let radioDiv = document.createElement('div');
                        radioDiv.classList.add('form-check');

                        let input = document.createElement('input');
                        input.type = 'radio';
                        input.classList.add('form-check-input');
                        input.name = 'hora';
                        input.value = hora;
                        input.id = `hora-${hora}`;
                        input.required = true;

                        let label = document.createElement('label');
                        label.classList.add('form-check-label');
                        label.htmlFor = `hora-${hora}`;
                        label.textContent = hora;

                        radioDiv.appendChild(input);
                        radioDiv.appendChild(label);
                        horaContainer.appendChild(radioDiv);
                    });
                });
        }
    });

    document.getElementById('citaForm').addEventListener('submit', function(e) {
        const fecha = document.getElementById('fecha').value;
        const horaInput = document.querySelector('input[name="hora"]:checked');
        const motivo = document.getElementById('motivo').value;

        if (!horaInput) {
            e.preventDefault();
            alert('Por favor, seleccione una hora.');
            return;
        }

        const hora = horaInput.value;
        console.log('Fecha:', fecha);
        console.log('Hora:', hora);
        console.log('Motivo:', motivo);
        this.submit();
    });
});

function confirmarCancelacion(citaId) {
    if (confirm('¿Estás seguro de cancelar el agendamiento de esta cita?')) {
        // Enviar una solicitud POST al servidor para actualizar la asistencia
        const url = `/cancelar-cita/${citaId}/`;
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                estado: 'cancelada'  // Estado deseado al actualizar la asistencia
            })
        })
        .then(response => {
            if (response.ok) {
                alert('Asistencia cancelada exitosamente.');
                location.reload();  // Recargar la página después de la actualización
            } else {
                alert('Ocurrió un error al actualizar la asistencia.');
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
            alert('Ocurrió un error en la solicitud.');
        });
    }
}


function confirmarActualizacion(citaId) {
    if (confirm('¿Estás seguro de actualizar la asistencia de esta cita?')) {
        // Enviar una solicitud POST al servidor para actualizar la asistencia
        const url = `/cancelar-cita/${citaId}/`;
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                estado: 'completada'  // Estado deseado al actualizar la asistencia
            })
        })
        .then(response => {
            if (response.ok) {
                alert('Asistencia actualizada exitosamente.');
                location.reload();  // Recargar la página después de la actualización
            } else {
                alert('Ocurrió un error al actualizar la asistencia.');
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
            alert('Ocurrió un error en la solicitud.');
        });
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}