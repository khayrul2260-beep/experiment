document.addEventListener("DOMContentLoaded", function () {

    const slider = document.getElementById("nfxVaultSlider");

    if (!slider) return;


    const slides = slider.querySelectorAll(
        ".mobile-hero-slide_"
    );

    const dots = slider.querySelectorAll(
        ".nfx-vault-dots button"
    );


    if (slides.length === 0) return;


    let currentIndex = 0;

    let autoSlideTimer = null;

    const slideDuration = 5000;


    /* =====================================================
       SHOW SLIDE
    ===================================================== */

    function showSlide(index) {

        if (index >= slides.length) {
            index = 0;
        }

        if (index < 0) {
            index = slides.length - 1;
        }


        currentIndex = index;


        /* Images */

        slides.forEach(function (slide, i) {

            slide.classList.toggle(
                "active",
                i === currentIndex
            );

        });


        /* Dots */

        dots.forEach(function (dot, i) {

            dot.classList.toggle(
                "is-active",
                i === currentIndex
            );

        });

    }


    /* =====================================================
       NEXT
    ===================================================== */

    function nextSlide() {

        showSlide(currentIndex + 1);

    }


    /* =====================================================
       START AUTO SLIDER
    ===================================================== */

    function startAutoSlide() {

        clearInterval(autoSlideTimer);


        autoSlideTimer = setInterval(function () {

            nextSlide();

        }, slideDuration);

    }


    /* =====================================================
       DOT CLICK
    ===================================================== */

    dots.forEach(function (dot, index) {

        dot.addEventListener("click", function () {

            showSlide(index);

            startAutoSlide();

        });

    });


    /* =====================================================
       INITIAL
    ===================================================== */

    showSlide(0);

    startAutoSlide();

});