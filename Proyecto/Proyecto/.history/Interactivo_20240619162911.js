// Obtenemos una lista de todos los slides
var slides = document.querySelectorAll('.slide');

// Función para mostrar un slide específico
function mostrarSlide(index) {
    // Ocultamos todos los slides
    for (var i = 0; i < slides.length; i++) {
        slides[i].style.display = 'none';
    }
    // Mostramos el slide deseado
    slides[index].style.display = 'block';
}

// Lógica para cambiar de slide al hacer clic en enlaces u otros controles
document.getElementById('slide1').addEventListener('click', function() {
    mostrarSlide(0); // Muestra el primer slide
});

document.getElementById('slide2').addEventListener('click', function() {
    mostrarSlide(1); // Muestra el segundo slide
});

document.getElementById('slide3').addEventListener('click', function() {
    mostrarSlide(2); // Muestra el tercer slide
});

// Mostramos el primer slide al cargar la página
mostrarSlide(0);

