function confirmarEliminacion(id) {
    const actionUrl = `/eliminarfechas/${id}/`;
    document.getElementById('formEliminar').action = actionUrl;
    document.getElementById('confirmarModal').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('confirmarModal').style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == document.getElementById('confirmarModal')) {
        cerrarModal();
    }
}