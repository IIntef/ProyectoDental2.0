// main.js

document.addEventListener('DOMContentLoaded', function() {

    function cancelarCita(citaId) {
        if (confirm('¿Estás seguro de cancelar el agendamiento de esta cita?')) {
            const url = `/cancelar-cita/${citaId}/`;
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => {
                if (response.ok) {
                    alert('Cita cancelada exitosamente.');
                    // Recargar horas disponibles después de cancelar la cita
                    const fechaSeleccionada = fechaInput.value; // Obtener la fecha seleccionada
                    if (fechaSeleccionada) {
                        cargarHorasDisponibles(fechaSeleccionada);
                    }
                } else {
                    alert('Ocurrió un error al cancelar la cita.');
                }
            })
            .catch(error => {
                console.error('Error en la solicitud:', error);
                alert('Ocurrió un error en la solicitud.');
            });
        }
    }

    function confirmarActualizacion(citaId) {
        if (confirm('¿Estás seguro de confirmar la actualización de esta cita?')) {
            const url = `/confirmar-actualizacion/${citaId}/`;
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => {
                if (response.ok) {
                    alert('Cita actualizada correctamente.');
                    // Recargar horas disponibles después de confirmar la actualización
                    const fechaSeleccionada = fechaInput.value; // Obtener la fecha seleccionada
                    if (fechaSeleccionada) {
                        cargarHorasDisponibles(fechaSeleccionada);
                    }
                } else {
                    alert('Ocurrió un error al confirmar la actualización de la cita.');
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

    // Event listener para botones de cancelar cita
    const cancelButtons = document.querySelectorAll('.cancelar-cita-btn');
    cancelButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const citaId = this.dataset.citaId;
            cancelarCita(citaId);
        });
    });

    // Event listener para botones de confirmar actualización
    const confirmButtons = document.querySelectorAll('.confirmar-actualizacion-btn');
    confirmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const citaId = this.dataset.citaId;
            confirmarActualizacion(citaId);
        });
    });

    const fechaInput = document.getElementById('fecha');
    const horaContainer = document.getElementById('hora');

    // Inicializar Flatpickr para el input de fecha
    flatpickr(fechaInput, {
        dateFormat: "Y-m-d",
        minDate: "today",
        inline: true,
        static: true,
        onChange: function(selectedDates, dateStr, instance) {
            const fechaValida = selectedDates.length > 0;

            if (fechaValida) {
                cargarHorasDisponibles(dateStr); // Cargar las horas disponibles al cambiar la fecha
            } else {
                horaContainer.innerHTML = '';  // Limpiar opciones si no hay fecha válida seleccionada
            }
        }
    });

    // Función para cargar las horas disponibles según la fecha seleccionada
    function cargarHorasDisponibles(fechaSeleccionada) {
        fetch(`/get-horas-disponibles/?fecha=${fechaSeleccionada}`)
            .then(response => response.json())
            .then(horas => {
                horaContainer.innerHTML = '';  // Limpiar opciones actuales
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
            })
            .catch(error => {
                console.error('Error al obtener horas disponibles:', error);
                alert('Ocurrió un error al obtener las horas disponibles.');
            });
    }

    // Cargar las horas disponibles inicialmente si hay una fecha seleccionada al inicio
    const fechaInicial = fechaInput.value;
    if (fechaInicial) {
        cargarHorasDisponibles(fechaInicial);
    }

});

