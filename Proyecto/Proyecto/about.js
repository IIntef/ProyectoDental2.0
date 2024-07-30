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

function openInNewTab(url) {
    var width = 600;
    var height = 400;
    var left = (screen.width - width) / 2;
    var top = (screen.height - height) / 2;

    window.open(url, '_blank', `toolbar=yes,scrollbars=yes,resizable=yes,top=${top},left=${left},width=${width},height=${height}`);
}