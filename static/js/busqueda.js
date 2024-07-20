document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const tipoDocumentoFilter = document.getElementById('tipoDocumentoFilter');
    const table = document.getElementById('patientTable');
    const rows = table.getElementsByTagName('tr');

    function filterTable() {
        const searchTerm = searchInput.value.toLowerCase();
        const tipoDocumento = tipoDocumentoFilter.value;

        console.log('Término de búsqueda:', searchTerm);
        console.log('Tipo de documento:', tipoDocumento);
        console.log('Número de filas:', rows.length);

        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const cells = row.getElementsByTagName('td');
            let shouldShow = true;

            if (searchTerm) {
                shouldShow = false;
                for (let cell of cells) {
                    if (cell.textContent.toLowerCase().includes(searchTerm)) {
                        shouldShow = true;
                        break;
                    }
                }
            }

            if (shouldShow && tipoDocumento) {
                shouldShow = cells[1].textContent.trim() === tipoDocumento;
            }

            row.style.display = shouldShow ? '' : 'none';
        }
    }

    searchInput.addEventListener('input', filterTable);
    tipoDocumentoFilter.addEventListener('change', filterTable);
});