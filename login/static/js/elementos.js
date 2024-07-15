function confirmarEliminacion(id, producto) {
    document.getElementById('elementoProducto').textContent = producto;
    const actionUrl = `/eliminarelementos/${id}/`;
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