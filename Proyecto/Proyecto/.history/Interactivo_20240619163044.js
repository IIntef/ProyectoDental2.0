var currentSlide = 1;

function showSlide(slideIndex) {
    var slides = document.getElementsByClassName("slide");
    if (slideIndex > slides.length) {
        currentSlide = 1;
    }
    if (slideIndex < 1) {
        currentSlide = slides.length;
    }
    for (var i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[currentSlide - 1].style.display = "block";
}

showSlide(currentSlide);

// Funciones para los botones de navegación (opcional)
document.querySelector('.prev').addEventListener('click', function() {
    showSlide(--currentSlide);
});

document.querySelector('.next').addEventListener('click', function() {
    showSlide(++currentSlide);
});
