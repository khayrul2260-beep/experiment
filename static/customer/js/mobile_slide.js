document.addEventListener("DOMContentLoaded", function () {

    const slides = document.querySelectorAll(".mobile-hero-slide");
    const dots = document.querySelectorAll(".hero-dot");

    if (!slides.length) return;

    let currentSlide = 0;

    function showSlide(index) {

        slides.forEach((slide, i) => {
            slide.classList.toggle("active", i === index);
        });

        dots.forEach((dot, i) => {
            dot.classList.toggle("active", i === index);
        });
    }


    function nextSlide() {

        currentSlide++;

        if (currentSlide >= slides.length) {
            currentSlide = 0;
        }

        showSlide(currentSlide);
    }


    /* Change image every 5 seconds */

    setInterval(nextSlide, 5000);

});
