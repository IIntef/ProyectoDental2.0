// Función para confirmar la eliminación de un elemento
function confirmarEliminacion(id, producto) {
    document.getElementById('elementoProducto').textContent = producto;
    const actionUrl = `/eliminarelementos/${id}/`;
    document.getElementById('formEliminar').action = actionUrl;
    document.getElementById('confirmarModal').style.display = 'block';
}

// Función para cerrar el modal de confirmación
function cerrarModal() {
    document.getElementById('confirmarModal').style.display = 'none';
}

// Cerrar el modal si se hace clic fuera del contenido del modal
window.onclick = function(event) {
    if (event.target == document.getElementById('confirmarModal')) {
        cerrarModal();
    }
}

// Función para filtrar la tabla
function filtrarTabla() {
    var searchValue = document.getElementById('searchInput').value.toLowerCase();
    var estadoValue = document.getElementById('estadoFilter').value;
    var table = document.getElementById('elementosTable');
    var rows = table.querySelector('tbody').getElementsByTagName('tr');

    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        var match = false;
        var estadoCell = cells[2].innerText; // Asumiendo que la columna de estado es la tercera (índice 2)

        // Verifica si el estado coincide con el filtro
        if (estadoValue === "" || estadoCell === estadoValue) {
            // Verifica si el texto de búsqueda coincide
            for (var j = 0; j < cells.length - 1; j++) {  // Excluye la columna de acciones
                if (cells[j].innerText.toLowerCase().indexOf(searchValue) > -1) {
                    match = true;
                    break;
                }
            }
        }

        rows[i].style.display = match ? '' : 'none';
    }
}

// Agrega eventos para filtrar la tabla
document.getElementById('searchInput').addEventListener('input', filtrarTabla);
document.getElementById('estadoFilter').addEventListener('change', filtrarTabla);

// Función para ordenar la tabla
document.querySelectorAll('th[data-sort]').forEach(function(header) {
    header.addEventListener('click', function() {
        var sortKey = header.getAttribute('data-sort');
        var table = document.getElementById('elementosTable');
        var tbody = table.querySelector('tbody');
        var rows = Array.from(tbody.querySelectorAll('tr'));

        // Alterna el orden de clasificación
        var sortOrder = header.dataset.order === 'asc' ? 'desc' : 'asc';
        header.dataset.order = sortOrder;

        rows.sort(function(rowA, rowB) {
            var cellA = rowA.querySelector('td[data-sort="' + sortKey + '"]').innerText;
            var cellB = rowB.querySelector('td[data-sort="' + sortKey + '"]').innerText;

            if (sortKey === 'cantidad') {
                cellA = parseFloat(cellA);
                cellB = parseFloat(cellB);
            }

            if (cellA < cellB) {
                return sortOrder === 'asc' ? -1 : 1;
            } else if (cellA > cellB) {
                return sortOrder === 'asc' ? 1 : -1;
            } else {
                return 0;
            }
        });

        rows.forEach(function(row) {
            tbody.appendChild(row);
        });

        // Actualiza la visualización del encabezado
        document.querySelectorAll('th[data-sort] i').forEach(function(icon) {
            icon.classList.remove('fa-arrow-up', 'fa-arrow-down');
            icon.classList.add('fa-arrow-down-short-wide'); // Reset icon to default
        });
        var icon = header.querySelector('i');
        icon.classList.remove('fa-arrow-down-short-wide');
        icon.classList.add(sortOrder === 'asc' ? 'fa-arrow-up' : 'fa-arrow-down');
        // Add animation
        icon.classList.add('animate');
        setTimeout(() => icon.classList.remove('animate'), 300); // Remove animation class after animation ends
    });
});

let currentPage = 1;
let itemsPerPage = parseInt(document.getElementById('itemsPerPage').value, 10);

function renderTable() {
    const table = document.getElementById('elementosTable');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    const totalRows = rows.length;
    const totalPages = Math.ceil(totalRows / itemsPerPage);

    // Ocultar todas las filas
    rows.forEach(row => row.style.display = 'none');

    // Mostrar solo las filas de la página actual
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    rows.slice(start, end).forEach(row => row.style.display = '');

    // Renderizar los controles de paginación
    renderPagination(totalPages);
}

function renderPagination(totalPages) {
    const paginationContainer = document.getElementById('pagination');
    paginationContainer.innerHTML = '';

    if (totalPages > 1) {
        // Crear botones de paginación
        const createButton = (text, page, isDisabled) => {
            const button = document.createElement('a');
            button.textContent = text;
            button.href = '#';
            button.className = `page-link ${isDisabled ? 'disabled' : ''}`;
            button.addEventListener('click', (event) => {
                event.preventDefault();
                if (!isDisabled) {
                    currentPage = page;
                    renderTable();
                }
            });
            return button;
        };

        // Botón de "Anterior"
        paginationContainer.appendChild(createButton('«', currentPage - 1, currentPage === 1));

        // Botones de página
        for (let i = 1; i <= totalPages; i++) {
            paginationContainer.appendChild(createButton(i, i, i === currentPage));
        }

        // Botón de "Siguiente"
        paginationContainer.appendChild(createButton('»', currentPage + 1, currentPage === totalPages));
    }
}

// Manejar el cambio en el número de elementos por página
document.getElementById('itemsPerPage').addEventListener('change', function() {
    itemsPerPage = parseInt(this.value, 10);
    currentPage = 1; // Reiniciar a la primera página cuando se cambia el número de elementos por página
    renderTable();
});

// Inicializar la tabla al cargar la página
renderTable();
