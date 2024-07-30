document.addEventListener('DOMContentLoaded', function() {
    var abrirVentana = document.getElementById('abrirVentana');
    var cerrarVentana = document.getElementById('cerrarVentana');
    var ventanaInformativa = document.getElementById('ventanaInformativa');

    abrirVentana.addEventListener('click', function(e) {
        e.preventDefault(); // Previene el comportamiento predeterminado del enlace
        ventanaInformativa.style.display = 'block';
    });

    cerrarVentana.addEventListener('click', function() {
        ventanaInformativa.style.display = 'none';
    });
});

