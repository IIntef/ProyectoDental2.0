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
                    return response.json();
                } else {
                    return response.json().then(err => {
                        throw new Error(err.message || 'Ocurrió un error al cancelar la cita.');
                    });
                }
            })
            .then(data => {
                alert('Cita cancelada exitosamente.');
                window.location.reload();
                actualizarInterfaz();
            })
            .catch(error => {
                console.error('Error en la solicitud:', error);
                alert(error.message);
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
                    return response.json();
                } else {
                    return response.json().then(err => {
                        throw new Error(err.message || 'Ocurrió un error al confirmar la actualización de la cita.');
                    });
                }
            })
            .then(data => {
                alert('Cita actualizada correctamente.');
                window.location.reload();
                actualizarInterfaz();
            })
            .catch(error => {
                console.error('Error en la solicitud:', error);
                alert(error.message);
            });
        }
    }

    function actualizarInterfaz() {
        // Actualizar la lista de citas
        actualizarListaCitas();
        // Actualizar las fechas y horas disponibles
        const fechaInput = document.getElementById('fecha');
        if (fechaInput && fechaInput.value) {
            cargarHorasDisponibles(fechaInput.value);
        }
    }

    function actualizarListaCitas() {
        fetch('/obtener-lista-citas/')
            .then(response => response.text())
            .then(html => {
                const listaCitasContainer = document.getElementById('lista-citas-container');
                if (listaCitasContainer) {
                    listaCitasContainer.innerHTML = html;
                    // Volver a agregar los event listeners a los nuevos botones
                    agregarEventListenersBotones();
                }
            })
            .catch(error => {
                console.error('Error al actualizar la lista de citas:', error);
            });
    }

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
                cargarHorasDisponibles(dateStr);
            } else {
                horaContainer.innerHTML = '';
            }
        }
    });

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

    // Inicializar los event listeners de los botones
    agregarEventListenersBotones();
});