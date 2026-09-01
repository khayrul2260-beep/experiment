document.addEventListener("DOMContentLoaded", function () {

    const slider = document.getElementById("mobileHeroSlider");

    if (!slider) {
        return;
    }


    const slides = slider.querySelectorAll(
        ".mobile-hero-slide"
    );

    const indicators = slider.querySelectorAll(
        ".mobile-slider-indicators button"
    );


    if (!slides.length) {
        return;
    }


    let currentSlide = 0;

    let slideTimer;


    function showSlide(index) {

        slides.forEach(function (slide, i) {

            slide.classList.toggle(
                "active",
                i === index
            );

        });


        indicators.forEach(function (indicator, i) {

            indicator.classList.toggle(
                "active",
                i === index
            );

        });


        currentSlide = index;
    }


    function nextSlide() {

        const next =
            (currentSlide + 1) % slides.length;

        showSlide(next);
    }


    function startSlider() {

        clearInterval(slideTimer);

        slideTimer = setInterval(
            nextSlide,
            3500
        );
    }


    indicators.forEach(function (indicator, index) {

        indicator.addEventListener(
            "click",
            function () {

                showSlide(index);

                startSlider();

            }
        );

    });


    showSlide(0);

    startSlider();


    /* -----------------------------------------------------
       TOUCH SWIPE
    ----------------------------------------------------- */

    let touchStartX = 0;

    let touchEndX = 0;


    slider.addEventListener(
        "touchstart",
        function (event) {

            touchStartX =
                event.changedTouches[0].screenX;

        },
        { passive: true }
    );


    slider.addEventListener(
        "touchend",
        function (event) {

            touchEndX =
                event.changedTouches[0].screenX;


            const difference =
                touchStartX - touchEndX;


            if (Math.abs(difference) < 50) {
                return;
            }


            if (difference > 0) {

                nextSlide();

            } else {

                const previous =
                    (currentSlide - 1 + slides.length)
                    % slides.length;

                showSlide(previous);
            }


            startSlider();

        },
        { passive: true }
    );

});