document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       REUSABLE INFINITE SLIDER
    ===================================================== */

    function initInfiniteSlider(
        sliderSelector,
        trackSelector,
        unavailableSelector = null
    ) {

        const slider = document.querySelector(sliderSelector);
        const track = document.querySelector(trackSelector);

        if (!slider || !track) {
            return;
        }


        /* =================================================
           ORIGINAL CARDS
        ================================================= */

        const originalCards = Array.from(track.children);

        if (!originalCards.length) {
            return;
        }


        /* =================================================
           CREATE CLONES
        ================================================= */

        function createGroup() {

            return originalCards.map(card =>
                card.cloneNode(true)
            );

        }


        const group1 = createGroup();
        const group2 = createGroup();
        const group3 = createGroup();


        /* =================================================
           REBUILD TRACK
        ================================================= */

        track.innerHTML = "";

        [
            ...group1,
            ...group2,
            ...group3
        ].forEach(card => {

            track.appendChild(card);

        });


        /* =================================================
           VARIABLES
        ================================================= */

        let loopWidth = 0;

        let isHovered = false;
        let isDragging = false;

        let animationFrame = null;

        let lastTime = performance.now();


        /*
           Same speed as existing
           Category Slider.
        */

        const autoSpeed = 0.7;


        /* =================================================
           CALCULATE LOOP WIDTH
        ================================================= */

        function calculateLoopWidth() {

            const firstCard =
                track.children[0];

            const secondGroupFirstCard =
                track.children[
                    originalCards.length
                ];


            if (
                !firstCard ||
                !secondGroupFirstCard
            ) {
                return;
            }


            loopWidth =
                secondGroupFirstCard.offsetLeft -
                firstCard.offsetLeft;

        }


        /* =================================================
           INITIAL POSITION
        ================================================= */

        requestAnimationFrame(function () {

            calculateLoopWidth();

            if (loopWidth > 0) {

                slider.scrollLeft =
                    loopWidth;

            }

        });


        /* =================================================
           INFINITE LOOP
        ================================================= */

        function normalizeLoop() {

            if (loopWidth <= 0) {
                return;
            }


            /*
               Third group → Second group
            */

            if (
                slider.scrollLeft >=
                loopWidth * 2
            ) {

                slider.scrollLeft -=
                    loopWidth;

            }


            /*
               First group → Second group
            */

            if (
                slider.scrollLeft <= 0
            ) {

                slider.scrollLeft +=
                    loopWidth;

            }

        }


        /* =================================================
           AUTO SCROLL
        ================================================= */

        function autoScroll(currentTime) {

            const delta =
                currentTime - lastTime;

            lastTime =
                currentTime;


            if (
                !isHovered &&
                !isDragging &&
                loopWidth > 0
            ) {

                slider.scrollLeft +=
                    autoSpeed *
                    (delta / 16.67);

            }


            normalizeLoop();


            animationFrame =
                requestAnimationFrame(
                    autoScroll
                );

        }


        animationFrame =
            requestAnimationFrame(
                autoScroll
            );


        /* =================================================
           MOUSE HOVER
        ================================================= */

        slider.addEventListener(
            "mouseenter",
            function () {

                isHovered = true;

            }
        );


        slider.addEventListener(
            "mouseleave",
            function () {

                isHovered = false;

            }
        );


        /* =================================================
           MOUSE DRAG
        ================================================= */

        let mouseStartX = 0;
        let mouseStartScroll = 0;
        let mouseMoved = false;


        slider.addEventListener(
            "mousedown",
            function (event) {

                isDragging = true;

                mouseMoved = false;

                mouseStartX =
                    event.clientX;

                mouseStartScroll =
                    slider.scrollLeft;


                slider.classList.add(
                    "is-dragging"
                );


                event.preventDefault();

            }
        );


        slider.addEventListener(
            "mousemove",
            function (event) {

                if (!isDragging) {
                    return;
                }


                const distance =
                    event.clientX -
                    mouseStartX;


                if (
                    Math.abs(distance) > 5
                ) {

                    mouseMoved = true;

                }


                slider.scrollLeft =
                    mouseStartScroll -
                    distance;


                normalizeLoop();

            }
        );


        function stopMouseDrag() {

            if (!isDragging) {
                return;
            }


            isDragging = false;


            slider.classList.remove(
                "is-dragging"
            );

        }


        document.addEventListener(
            "mouseup",
            stopMouseDrag
        );


        /* =================================================
           PREVENT CLICK AFTER DRAG
        ================================================= */

        slider.addEventListener(
            "click",
            function (event) {

                if (mouseMoved) {

                    event.preventDefault();

                    event.stopPropagation();

                    mouseMoved = false;

                }

            },
            true
        );


        /* =================================================
           TOUCH SWIPE
        ================================================= */

        let touchStartX = 0;
        let touchStartScroll = 0;
        let touchMoved = false;


        slider.addEventListener(
            "touchstart",
            function (event) {

                isDragging = true;

                touchMoved = false;


                touchStartX =
                    event.touches[0].clientX;

                touchStartScroll =
                    slider.scrollLeft;

            },
            {
                passive: true
            }
        );


        slider.addEventListener(
            "touchmove",
            function (event) {

                if (!isDragging) {
                    return;
                }


                const currentX =
                    event.touches[0].clientX;


                const distance =
                    currentX -
                    touchStartX;


                if (
                    Math.abs(distance) > 5
                ) {

                    touchMoved = true;

                }


                slider.scrollLeft =
                    touchStartScroll -
                    distance;


                normalizeLoop();

            },
            {
                passive: true
            }
        );


        slider.addEventListener(
            "touchend",
            function () {

                isDragging = false;


                if (touchMoved) {

                    mouseMoved = true;

                }


                touchMoved = false;

            }
        );


        /* =================================================
           UNAVAILABLE ITEMS
        ================================================= */

        if (unavailableSelector) {

            const unavailableItems =
                track.querySelectorAll(
                    unavailableSelector
                );


            unavailableItems.forEach(item => {

                item.addEventListener(
                    "click",
                    function (event) {

                        event.preventDefault();

                        event.stopPropagation();

                    }
                );

            });

        }


        /* =================================================
           RESIZE
        ================================================= */

        let resizeTimer;


        window.addEventListener(
            "resize",
            function () {

                clearTimeout(
                    resizeTimer
                );


                resizeTimer =
                    setTimeout(
                        function () {

                            calculateLoopWidth();


                            if (
                                loopWidth > 0 &&
                                slider.scrollLeft <= 0
                            ) {

                                slider.scrollLeft =
                                    loopWidth;

                            }

                        },
                        200
                    );

            }
        );

    }


    /* =====================================================
       CATEGORY SLIDER
    ===================================================== */

    initInfiniteSlider(
        ".mobile-category-slider",
        ".mobile-category-grid",
        ".category-unavailable"
    );


    /* =====================================================
       ALL PRODUCTS SLIDER
    ===================================================== */

    initInfiniteSlider(
        ".mobile-all-products-slider",
        ".mobile-all-products-grid"
    );

});