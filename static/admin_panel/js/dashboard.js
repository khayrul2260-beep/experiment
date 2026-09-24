/* ============================================================
   NAFI ADMIN DASHBOARD
   dashboard.js
   ============================================================ */

(function () {

    "use strict";


    /* ========================================================
       DOM READY
    ======================================================== */

    document.addEventListener("DOMContentLoaded", function () {

        initializeDashboard();

    });


    /* ========================================================
       MAIN INITIALIZER
    ======================================================== */

    function initializeDashboard() {

        initializeRevenueFilters();

        initializePanelLinks();

        initializeTableScroll();

        initializeQuickActions();

        initializeKpiHover();

    }


    /* ========================================================
       REVENUE FILTERS
    ======================================================== */

    function initializeRevenueFilters() {

        const form = document.getElementById("revenueFilterForm");

        if (!form) {
            return;
        }


        const yearSelect = document.getElementById("revenueYear");

        const monthSelect = document.getElementById("revenueMonth");

        const weekSelect = document.getElementById("revenueWeek");

        const daySelect = document.getElementById("revenueDay");


        /*
         * Keep the selected filter values when the page reloads.
         * Django is responsible for generating the available
         * year / month / week / day options.
         */

        if (yearSelect) {

            yearSelect.addEventListener("change", function () {

                /*
                 * Changing year invalidates lower-level selections.
                 */

                if (monthSelect) {
                    monthSelect.value = "";
                }

                if (weekSelect) {
                    weekSelect.value = "";
                }

                if (daySelect) {
                    daySelect.value = "";
                }

                submitRevenueForm(form);

            });

        }


        if (monthSelect) {

            monthSelect.addEventListener("change", function () {

                if (weekSelect) {
                    weekSelect.value = "";
                }

                if (daySelect) {
                    daySelect.value = "";
                }

                /*
                 * Month selection can immediately submit.
                 */

                submitRevenueForm(form);

            });

        }


        if (weekSelect) {

            weekSelect.addEventListener("change", function () {

                if (daySelect) {
                    daySelect.value = "";
                }

            });

        }


        /*
         * Day selection does not automatically submit.
         * User can select day and press APPLY.
         */

    }


    /* ========================================================
       FORM SUBMIT
    ======================================================== */

    function submitRevenueForm(form) {

        if (!form) {
            return;
        }


        /*
         * Small visual feedback before navigation.
         */

        const applyButton =
            form.querySelector(".revenue-filter-apply");


        if (applyButton) {

            applyButton.disabled = true;

            applyButton.style.opacity = "0.6";

            applyButton.textContent = "LOADING";

        }


        /*
         * Native submit keeps the request simple and
         * compatible with Django.
         */

        form.submit();

    }


    /* ========================================================
       PANEL LINKS
    ======================================================== */

    function initializePanelLinks() {

        const links =
            document.querySelectorAll(
                ".nafi-dashboard a"
            );


        links.forEach(function (link) {

            link.addEventListener("click", function () {

                link.classList.add("dashboard-link-loading");

            });

        });

    }


    /* ========================================================
       TABLE HORIZONTAL SCROLL
    ======================================================== */

    function initializeTableScroll() {

        const wrappers =
            document.querySelectorAll(
                ".orders-table-wrapper, .top-products-table-wrapper"
            );


        wrappers.forEach(function (wrapper) {

            /*
             * Prevent accidental page movement while horizontally
             * scrolling large tables on touch devices.
             */

            wrapper.addEventListener(
                "wheel",
                function (event) {

                    if (
                        Math.abs(event.deltaY) >
                        Math.abs(event.deltaX)
                    ) {

                        if (
                            wrapper.scrollWidth >
                            wrapper.clientWidth
                        ) {

                            wrapper.scrollLeft += event.deltaY;

                            event.preventDefault();

                        }

                    }

                },
                {
                    passive: false
                }
            );

        });

    }


    /* ========================================================
       QUICK ACTIONS
    ======================================================== */

    function initializeQuickActions() {

        const actions =
            document.querySelectorAll(
                ".quick-action"
            );


        actions.forEach(function (action) {

            action.addEventListener(
                "mouseenter",
                function () {

                    const arrow =
                        action.querySelector(
                            ".quick-action-arrow"
                        );


                    if (arrow) {

                        arrow.style.transform =
                            "translateX(3px)";

                    }

                }
            );


            action.addEventListener(
                "mouseleave",
                function () {

                    const arrow =
                        action.querySelector(
                            ".quick-action-arrow"
                        );


                    if (arrow) {

                        arrow.style.transform =
                            "translateX(0)";

                    }

                }
            );

        });

    }


    /* ========================================================
       KPI HOVER
    ======================================================== */

    function initializeKpiHover() {

        const cards =
            document.querySelectorAll(
                ".dashboard-kpi-card"
            );


        cards.forEach(function (card) {

            card.addEventListener(
                "mouseenter",
                function () {

                    card.classList.add(
                        "kpi-card-active"
                    );

                }
            );


            card.addEventListener(
                "mouseleave",
                function () {

                    card.classList.remove(
                        "kpi-card-active"
                    );

                }
            );

        });

    }


    /* ========================================================
       PUBLIC HELPERS
    ======================================================== */

    window.NAFIDashboard = {

        refresh: function () {

            window.location.reload();

        },

        submitRevenue: function () {

            const form =
                document.getElementById(
                    "revenueFilterForm"
                );


            submitRevenueForm(form);

        }

    };

})();