"use strict";

/* =========================================================
   NAFI ADMIN DASHBOARD
   Professional Dashboard Interactions
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    initSidebar();
    initActiveMenu();
    initSearchBox();
    initCounterAnimation();
    initRevenuePeriod();
    initRevenueChart();
});


/* =========================================================
   SIDEBAR
========================================================= */

function initSidebar() {
    const sidebar = document.querySelector(".sidebar");
    const toggle = document.querySelector(".sidebar-toggle");

    if (!sidebar || !toggle) return;

    toggle.addEventListener("click", (event) => {
        event.stopPropagation();
        sidebar.classList.toggle("active");
    });

    /*
     * Close sidebar when clicking outside
     * on smaller screens.
     */
    document.addEventListener("click", (event) => {
        if (window.innerWidth > 992) return;

        const clickedInsideSidebar = sidebar.contains(event.target);
        const clickedToggle = toggle.contains(event.target);

        if (!clickedInsideSidebar && !clickedToggle) {
            sidebar.classList.remove("active");
        }
    });
}


/* =========================================================
   ACTIVE SIDEBAR MENU
========================================================= */

function initActiveMenu() {
    const menuItems = document.querySelectorAll(
        ".sidebar-menu li, .sidebar-menu a"
    );

    if (!menuItems.length) return;

    menuItems.forEach((item) => {
        item.addEventListener("click", () => {

            /*
             * Do not interfere with dropdown/menu groups.
             */
            if (item.tagName.toLowerCase() === "a") {
                const parent = item.closest("li");

                if (parent) {
                    document
                        .querySelectorAll(".sidebar-menu li")
                        .forEach((menu) => {
                            if (
                                menu !== parent &&
                                !menu.classList.contains("has-submenu")
                            ) {
                                menu.classList.remove("active");
                            }
                        });

                    parent.classList.add("active");
                }
            }
        });
    });
}


/* =========================================================
   SEARCH BOX
========================================================= */

function initSearchBox() {
    const searchInput = document.querySelector(".search-box input");

    if (!searchInput) return;

    searchInput.addEventListener("input", function () {
        const value = this.value.trim().toLowerCase();

        /*
         * Dashboard search is currently UI-ready.
         * Actual global search can be connected later.
         */
        if (!value) {
            searchInput.classList.remove("has-value");
            return;
        }

        searchInput.classList.add("has-value");
    });

    /*
     * Clear search state when pressing Escape.
     */
    searchInput.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            searchInput.value = "";
            searchInput.classList.remove("has-value");
            searchInput.blur();
        }
    });
}


/* =========================================================
   KPI COUNTER ANIMATION
========================================================= */

function initCounterAnimation() {
    const counters = document.querySelectorAll(
        ".stat-content h2, .stat-value, .kpi-value"
    );

    if (!counters.length) return;

    counters.forEach((counter) => {
        animateCounter(counter);
    });
}


function animateCounter(element) {
    const originalText = element.textContent.trim();

    if (!originalText) return;

    /*
     * Detect currency.
     */
    const hasCurrency = originalText.includes("৳");
    const hasDollar = originalText.includes("$");

    /*
     * Extract numeric value.
     */
    const numericString = originalText
        .replace(/[৳$,\s]/g, "");

    const target = parseFloat(numericString);

    if (!Number.isFinite(target)) return;

    /*
     * Prevent re-animation.
     */
    if (element.dataset.counterAnimated === "true") {
        return;
    }

    element.dataset.counterAnimated = "true";

    const duration = 850;
    const startTime = performance.now();

    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;

        const progress = Math.min(elapsed / duration, 1);

        /*
         * Smooth ease-out.
         */
        const easedProgress =
            1 - Math.pow(1 - progress, 3);

        const currentValue =
            target * easedProgress;

        let formattedValue;

        if (Number.isInteger(target)) {
            formattedValue =
                Math.floor(currentValue).toLocaleString("en-US");
        } else {
            formattedValue =
                currentValue.toLocaleString("en-US", {
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 2
                });
        }

        if (hasCurrency) {
            formattedValue = `৳${formattedValue}`;
        } else if (hasDollar) {
            formattedValue = `$${formattedValue}`;
        }

        element.textContent = formattedValue;

        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        } else {
            /*
             * Restore exact final value.
             */
            if (hasCurrency) {
                element.textContent =
                    `৳${target.toLocaleString("en-US")}`;
            } else if (hasDollar) {
                element.textContent =
                    `$${target.toLocaleString("en-US")}`;
            } else {
                element.textContent =
                    target.toLocaleString("en-US");
            }
        }
    }

    requestAnimationFrame(updateCounter);
}


/* =========================================================
   REVENUE PERIOD SELECTOR
========================================================= */

function initRevenuePeriod() {
    const select = document.getElementById("revenuePeriod");

    if (!select) return;

    select.addEventListener("change", function () {
        const selectedValue = this.value;

        if (!selectedValue) return;

        /*
         * Preserve existing query parameters.
         */
        const url = new URL(window.location.href);

        url.searchParams.set(
            "revenue_period",
            selectedValue
        );

        /*
         * Reload page with selected period.
         *
         * Revenue values are calculated by Django,
         * so no fake frontend data is used.
         */
        window.location.href = url.toString();
    });
}


/* =========================================================
   REVENUE CHART
========================================================= */

function initRevenueChart() {
    const canvas = document.getElementById("salesChart");

    if (!canvas) return;

    /*
     * Chart.js must be available.
     */
    if (typeof Chart === "undefined") {
        console.warn(
            "Chart.js is not loaded."
        );
        return;
    }

    /*
     * Django json_script data.
     */
    const labelsElement =
        document.getElementById("revenue-labels");

    const valuesElement =
        document.getElementById("revenue-values");

    if (!labelsElement || !valuesElement) {
        console.warn(
            "Revenue chart data was not found."
        );
        return;
    }

    let labels = [];
    let values = [];

    try {
        labels = JSON.parse(
            labelsElement.textContent
        );

        values = JSON.parse(
            valuesElement.textContent
        );
    } catch (error) {
        console.error(
            "Unable to parse revenue chart data:",
            error
        );
        return;
    }

    /*
     * Validate arrays.
     */
    if (
        !Array.isArray(labels) ||
        !Array.isArray(values)
    ) {
        console.warn(
            "Revenue chart data must be arrays."
        );
        return;
    }

    /*
     * Make sure both arrays have matching length.
     */
    const dataLength = Math.min(
        labels.length,
        values.length
    );

    labels = labels.slice(0, dataLength);
    values = values
        .slice(0, dataLength)
        .map((value) => Number(value) || 0);

    /*
     * Destroy an existing chart attached to this canvas.
     *
     * This protects against duplicate initialization
     * if the dashboard is dynamically reloaded.
     */
    const existingChart =
        Chart.getChart(canvas);

    if (existingChart) {
        existingChart.destroy();
    }

    const context =
        canvas.getContext("2d");

    if (!context) return;


    /* =====================================================
       GRADIENT
    ===================================================== */

    const gradient =
        context.createLinearGradient(
            0,
            0,
            0,
            canvas.clientHeight || 320
        );

    gradient.addColorStop(
        0,
        "rgba(37, 99, 235, 0.28)"
    );

    gradient.addColorStop(
        0.55,
        "rgba(37, 99, 235, 0.08)"
    );

    gradient.addColorStop(
        1,
        "rgba(37, 99, 235, 0)"
    );


    /* =====================================================
       CHART CONFIGURATION
    ===================================================== */

    new Chart(context, {
        type: "line",

        data: {
            labels: labels,

            datasets: [
                {
                    label: "Revenue",

                    data: values,

                    borderColor: "#2563EB",

                    backgroundColor: gradient,

                    borderWidth: 2.5,

                    fill: true,

                    tension: 0.42,

                    cubicInterpolationMode:
                        "monotone",

                    pointRadius: 0,

                    pointHoverRadius: 5,

                    pointHoverBorderWidth: 2,

                    pointHoverBackgroundColor:
                        "#ffffff",

                    pointHoverBorderColor:
                        "#2563EB",

                    spanGaps: true
                }
            ]
        },


        /* =================================================
           OPTIONS
        ================================================= */

        options: {

            responsive: true,

            maintainAspectRatio: false,

            interaction: {
                mode: "index",
                intersect: false
            },

            animation: {
                duration: 900,

                easing: "easeOutQuart"
            },

            plugins: {

                legend: {
                    display: false
                },

                tooltip: {

                    enabled: true,

                    backgroundColor:
                        "rgba(10, 10, 10, 0.96)",

                    titleColor:
                        "#F8FAFC",

                    bodyColor:
                        "#CBD5E1",

                    borderColor:
                        "rgba(255,255,255,0.08)",

                    borderWidth: 1,

                    padding: 11,

                    displayColors: false,

                    titleFont: {
                        family:
                            "Poppins, sans-serif",
                        size: 10,
                        weight: "500"
                    },

                    bodyFont: {
                        family:
                            "Poppins, sans-serif",
                        size: 11,
                        weight: "600"
                    },

                    callbacks: {

                        label: function (context) {
                            const value =
                                Number(context.raw) || 0;

                            return (
                                "Revenue: ৳" +
                                value.toLocaleString(
                                    "en-US"
                                )
                            );
                        }
                    }
                }
            },


            /* =================================================
               SCALES
            ================================================= */

            scales: {

                x: {

                    grid: {
                        display: false,
                        drawBorder: false
                    },

                    border: {
                        display: false
                    },

                    ticks: {

                        color:
                            "rgba(148, 163, 184, 0.8)",

                        font: {
                            family:
                                "Poppins, sans-serif",
                            size: 9,
                            weight: "400"
                        },

                        maxRotation: 0,

                        autoSkip: true,

                        autoSkipPadding: 14
                    }
                },


                y: {

                    beginAtZero: true,

                    grid: {

                        color:
                            "rgba(255,255,255,0.055)",

                        drawBorder: false,

                        lineWidth: 1
                    },

                    border: {
                        display: false
                    },

                    ticks: {

                        color:
                            "rgba(148, 163, 184, 0.8)",

                        padding: 8,

                        font: {
                            family:
                                "Poppins, sans-serif",
                            size: 9,
                            weight: "400"
                        },

                        callback: function (value) {
                            return formatRevenueAxis(
                                value
                            );
                        }
                    }
                }
            }
        }
    });
}


/* =========================================================
   REVENUE AXIS FORMATTER
========================================================= */

function formatRevenueAxis(value) {
    const number = Number(value) || 0;

    if (number >= 1000000) {
        return (
            "৳" +
            (number / 1000000)
                .toFixed(1)
                .replace(".0", "") +
            "M"
        );
    }

    if (number >= 1000) {
        return (
            "৳" +
            (number / 1000)
                .toFixed(1)
                .replace(".0", "") +
            "K"
        );
    }

    return "৳" + number.toLocaleString("en-US");
}


/* =========================================================
   RESPONSIVE CHART
========================================================= */

let resizeTimer = null;

window.addEventListener("resize", () => {

    /*
     * Close mobile sidebar on desktop.
     */
    const sidebar =
        document.querySelector(".sidebar");

    if (
        sidebar &&
        window.innerWidth > 992
    ) {
        sidebar.classList.remove("active");
    }

    /*
     * Avoid excessive resize calculations.
     */
    clearTimeout(resizeTimer);

    resizeTimer = setTimeout(() => {

        if (
            typeof Chart !== "undefined"
        ) {
            const chart =
                Chart.getChart("salesChart");

            if (chart) {
                chart.resize();
            }
        }

    }, 150);
});


/* =========================================================
   ACCESSIBILITY
========================================================= */

document.addEventListener(
    "keydown",
    (event) => {

        /*
         * Close mobile sidebar with Escape.
         */
        if (event.key !== "Escape") return;

        const sidebar =
            document.querySelector(".sidebar");

        if (
            sidebar &&
            window.innerWidth <= 992
        ) {
            sidebar.classList.remove("active");
        }
    }
);


/* =========================================================
   END OF DASHBOARD JS
========================================================= */