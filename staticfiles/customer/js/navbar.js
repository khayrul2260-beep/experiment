document.addEventListener("DOMContentLoaded", function () {


    /* =====================================================
       ELEMENTS
    ===================================================== */

    const navbar = document.getElementById("nafiNavbar");

    const mobileToggle =
        document.getElementById("nafiMobileToggle");

    const mobileMenu =
        document.getElementById("nafiMobileMenu");

    const mobileClose =
        document.getElementById("nafiMobileClose");

    const mobileOverlay =
        document.getElementById("nafiMobileOverlay");


    /* =====================================================
       DESKTOP DROPDOWNS
    ===================================================== */

    const dropdowns =
        document.querySelectorAll(".nav-dropdown");


    dropdowns.forEach(function (dropdown) {

        const trigger =
            dropdown.querySelector(".dropdown-trigger");


        if (!trigger) {
            return;
        }


        trigger.addEventListener("click", function (event) {

            event.preventDefault();

            event.stopPropagation();


            const isOpen =
                dropdown.classList.contains("dropdown-open");


            /* Close all other dropdowns */

            dropdowns.forEach(function (item) {

                item.classList.remove("dropdown-open");

                const itemTrigger =
                    item.querySelector(".dropdown-trigger");

                if (itemTrigger) {

                    itemTrigger.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }

            });


            /* Open clicked dropdown */

            if (!isOpen) {

                dropdown.classList.add("dropdown-open");

                trigger.setAttribute(
                    "aria-expanded",
                    "true"
                );

            }

        });

    });


    /* =====================================================
       CLOSE DROPDOWN WHEN CLICKING OUTSIDE
    ===================================================== */

    document.addEventListener("click", function (event) {

        if (
            !event.target.closest(".nav-dropdown")
        ) {

            dropdowns.forEach(function (dropdown) {

                dropdown.classList.remove(
                    "dropdown-open"
                );


                const trigger =
                    dropdown.querySelector(
                        ".dropdown-trigger"
                    );


                if (trigger) {

                    trigger.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }

            });

        }

    });


    /* =====================================================
       MOBILE MENU OPEN
    ===================================================== */

    function openMobileMenu() {

        if (!mobileMenu) {
            return;
        }


        mobileMenu.classList.add("mobile-open");


        if (mobileOverlay) {

            mobileOverlay.classList.add(
                "mobile-open"
            );

        }


        document.body.classList.add(
            "nafi-menu-open"
        );


        if (mobileToggle) {

            mobileToggle.setAttribute(
                "aria-expanded",
                "true"
            );

        }


        mobileMenu.setAttribute(
            "aria-hidden",
            "false"
        );

    }


    /* =====================================================
       MOBILE MENU CLOSE
    ===================================================== */

    function closeMobileMenu() {

        if (!mobileMenu) {
            return;
        }


        mobileMenu.classList.remove(
            "mobile-open"
        );


        if (mobileOverlay) {

            mobileOverlay.classList.remove(
                "mobile-open"
            );

        }


        document.body.classList.remove(
            "nafi-menu-open"
        );


        if (mobileToggle) {

            mobileToggle.setAttribute(
                "aria-expanded",
                "false"
            );

        }


        mobileMenu.setAttribute(
            "aria-hidden",
            "true"
        );


        /* Close mobile dropdowns */

        const mobileDropdowns =
            document.querySelectorAll(
                ".mobile-nav-dropdown"
            );


        mobileDropdowns.forEach(
            function (dropdown) {

                dropdown.classList.remove(
                    "dropdown-open"
                );


                const trigger =
                    dropdown.querySelector(
                        ".mobile-dropdown-trigger"
                    );


                if (trigger) {

                    trigger.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }

            }
        );

    }


    /* =====================================================
       MOBILE TOGGLE BUTTON
    ===================================================== */

    if (mobileToggle) {

        mobileToggle.addEventListener(
            "click",
            function () {

                const isOpen =
                    mobileMenu &&
                    mobileMenu.classList.contains(
                        "mobile-open"
                    );


                if (isOpen) {

                    closeMobileMenu();

                } else {

                    openMobileMenu();

                }

            }
        );

    }


    /* =====================================================
       MOBILE CLOSE BUTTON
    ===================================================== */

    if (mobileClose) {

        mobileClose.addEventListener(
            "click",
            function () {

                closeMobileMenu();

            }
        );

    }


    /* =====================================================
       MOBILE OVERLAY CLICK
    ===================================================== */

    if (mobileOverlay) {

        mobileOverlay.addEventListener(
            "click",
            function () {

                closeMobileMenu();

            }
        );

    }


    /* =====================================================
       MOBILE DROPDOWNS
    ===================================================== */

    const mobileDropdowns =
        document.querySelectorAll(
            ".mobile-nav-dropdown"
        );


    mobileDropdowns.forEach(function (dropdown) {

        const trigger =
            dropdown.querySelector(
                ".mobile-dropdown-trigger"
            );


        if (!trigger) {
            return;
        }


        trigger.addEventListener(
            "click",
            function () {

                const isOpen =
                    dropdown.classList.contains(
                        "dropdown-open"
                    );


                /* Close other mobile dropdowns */

                mobileDropdowns.forEach(
                    function (item) {

                        item.classList.remove(
                            "dropdown-open"
                        );


                        const itemTrigger =
                            item.querySelector(
                                ".mobile-dropdown-trigger"
                            );


                        if (itemTrigger) {

                            itemTrigger.setAttribute(
                                "aria-expanded",
                                "false"
                            );

                        }

                    }
                );


                /* Open clicked dropdown */

                if (!isOpen) {

                    dropdown.classList.add(
                        "dropdown-open"
                    );


                    trigger.setAttribute(
                        "aria-expanded",
                        "true"
                    );

                }

            }
        );

    });


    /* =====================================================
       ESC KEY
    ===================================================== */

    document.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Escape") {

                /* Close desktop dropdowns */

                dropdowns.forEach(
                    function (dropdown) {

                        dropdown.classList.remove(
                            "dropdown-open"
                        );


                        const trigger =
                            dropdown.querySelector(
                                ".dropdown-trigger"
                            );


                        if (trigger) {

                            trigger.setAttribute(
                                "aria-expanded",
                                "false"
                            );

                        }

                    }
                );


                /* Close mobile menu */

                closeMobileMenu();

            }

        }
    );


    /* =====================================================
       NAVBAR SCROLL EFFECT
    ===================================================== */

    function handleNavbarScroll() {

        if (!navbar) {
            return;
        }


        if (window.scrollY > 30) {

            navbar.classList.add(
                "navbar-scrolled"
            );

        } else {

            navbar.classList.remove(
                "navbar-scrolled"
            );

        }

    }


    window.addEventListener(
        "scroll",
        handleNavbarScroll,
        { passive: true }
    );


    /* Run once when page loads */

    handleNavbarScroll();


    /* =====================================================
       CLOSE MOBILE MENU WHEN RESIZING TO DESKTOP
    ===================================================== */

    window.addEventListener(
        "resize",
        function () {

            if (window.innerWidth > 991) {

                closeMobileMenu();

            }

        }
    );


});