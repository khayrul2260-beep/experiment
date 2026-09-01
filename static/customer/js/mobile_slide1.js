document.addEventListener("DOMContentLoaded", function () {

    /* =========================================================
       NFX VAULT HERO SLIDER
       Independent Slider System
    ========================================================= */

    const slider = document.getElementById("nfxVaultSlider");

    if (!slider) return;


    /* =========================================================
       SLIDES
    ========================================================= */

    const slides = slider.querySelectorAll(
        ".nfx-vault-panel"
    );


    /* =========================================================
       DOTS
    ========================================================= */

    const dots = slider.querySelectorAll(
        ".nfx-vault-dots button"
    );


    /* =========================================================
       SAFETY CHECK
    ========================================================= */

    if (!slides.length) return;


    /* =========================================================
       SETTINGS
    ========================================================= */

    let currentSlide = 0;

    const slideInterval = 5000;

    let autoSlideTimer;


    /* =========================================================
       SHOW SLIDE
    ========================================================= */

    function showVaultSlide(index) {

        /* Keep index within range */

        if (index < 0) {
            index = slides.length - 1;
        }

        if (index >= slides.length) {
            index = 0;
        }


        currentSlide = index;


        /* -----------------------------------------
           Update slides
        ----------------------------------------- */

        slides.forEach(function (slide, i) {

            slide.classList.toggle(
                "is-active",
                i === currentSlide
            );

        });


        /* -----------------------------------------
           Update dots
        ----------------------------------------- */

        dots.forEach(function (dot, i) {

            dot.classList.toggle(
                "is-active",
                i === currentSlide
            );

        });

    }


    /* =========================================================
       NEXT SLIDE
    ========================================================= */

    function goToNextVaultSlide() {

        const nextIndex =
            (currentSlide + 1) % slides.length;

        showVaultSlide(nextIndex);

    }


    /* =========================================================
       START AUTO SLIDER
    ========================================================= */

    function startVaultSlider() {

        clearInterval(autoSlideTimer);

        autoSlideTimer = setInterval(
            goToNextVaultSlide,
            slideInterval
        );

    }


    /* =========================================================
       DOT CLICK
    ========================================================= */

    dots.forEach(function (dot, index) {

        dot.addEventListener(
            "click",
            function () {

                showVaultSlide(index);

                /*
                   Restart timer so the next automatic
                   slide happens 5 seconds after the click.
                */

                startVaultSlider();

            }
        );

    });


    /* =========================================================
       INITIALIZE
    ========================================================= */

    showVaultSlide(0);

    startVaultSlider();


});