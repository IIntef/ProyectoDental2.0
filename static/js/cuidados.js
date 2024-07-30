var swiper = new Swiper(".mySwiper", {
    effect: "coverflow",
    grabCursor: true,
    centeredSlides: true,
    slidesPerView: "auto",
    loop: true,
    coverflowEffect: {
        rotate: 0,
        stretch: 0,
        depth: 500,
        modifier: 1,
        slideShadows: true
    },
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    autoplay: {
        delay: 3000, 
        disableOnInteraction: false,
    },
});
document.querySelector('.mySwiper').addEventListener('mouseenter', function() {
    swiper.autoplay.stop();
});
document.querySelector('.mySwiper').addEventListener('mouseleave', function() {
    swiper.autoplay.start();
});