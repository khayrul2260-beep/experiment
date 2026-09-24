"use strict";

/* =========================================================
   NAFI ADMIN DASHBOARD
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    sidebarToggle();

    activeMenu();

    searchBox();

    counterAnimation();

    revenuePeriodSelector();

    dashboardChart();

});

/* =========================================================
   SIDEBAR TOGGLE
========================================================= */

function sidebarToggle() {

    const sidebar = document.querySelector(".sidebar");
    const toggle = document.querySelector(".sidebar-toggle");

    if (!sidebar || !toggle) return;

    toggle.addEventListener("click", () => {
        sidebar.classList.toggle("active");
    });

}


/* =========================================================
   ACTIVE MENU
========================================================= */

function activeMenu() {

    const menuItems = document.querySelectorAll(".sidebar-menu li");

    if (!menuItems.length) return;

    menuItems.forEach((item) => {

        item.addEventListener("click", () => {

            menuItems.forEach((menu) => {
                menu.classList.remove("active");
            });

            item.classList.add("active");

        });

    });

}


/* =========================================================
   SEARCH BOX
========================================================= */

function searchBox() {

    const searchInput = document.querySelector(".search-box input");

    if (!searchInput) return;

    searchInput.addEventListener("input", function () {

        const value = this.value.trim();

        /*
         * Global dashboard search can be connected later.
         * For now, keep the input lightweight.
         */

        if (value.length > 0) {
            console.log("Dashboard Search:", value);
        }

    });

}


/* =========================================================
   KPI COUNTER ANIMATION
========================================================= */

function counterAnimation() {

    const counters = document.querySelectorAll(
        ".dashboard-kpi-value"
    );

    if (!counters.length) return;

    counters.forEach((counter) => {

        const originalText = counter.textContent.trim();

        /*
         * Detect currency.
         */
        const isCurrency = originalText.includes("৳");

        /*
         * Extract number.
         */
        const number = parseFloat(
            originalText
                .replace(/[^\d.]/g, "")
        );

        if (isNaN(number)) return;

        /*
         * Decimal values do not need animation.
         */
        if (!Number.isInteger(number)) return;

        let current = 0;

        const duration = 900;

        const startTime = performance.now();

        function updateCounter(currentTime) {

            const elapsed = currentTime - startTime;

            const progress = Math.min(
                elapsed / duration,
                1
            );

            /*
             * Ease-out effect.
             */
            const easedProgress =
                1 - Math.pow(1 - progress, 3);

            current = Math.floor(
                number * easedProgress
            );

            if (isCurrency) {

                counter.textContent =
                    "৳" +
                    current.toLocaleString("en-BD");

            } else {

                counter.textContent =
                    current.toLocaleString("en-BD");

            }

            if (progress < 1) {

                requestAnimationFrame(
                    updateCounter
                );

            } else {

                if (isCurrency) {

                    counter.textContent =
                        "৳" +
                        number.toLocaleString("en-BD");

                } else {

                    counter.textContent =
                        number.toLocaleString("en-BD");

                }

            }

        }

        requestAnimationFrame(updateCounter);

    });

}


/* =========================================================
   SALES / REVENUE CHART
========================================================= */
/* =========================================================
   REAL REVENUE CHART
========================================================= */

function dashboardChart() {

    const canvas =
        document.getElementById("salesChart");

    if (!canvas) return;

    if (typeof Chart === "undefined") {

        console.warn(
            "Chart.js is not loaded."
        );

        return;

    }


    const labelsElement =
        document.getElementById(
            "revenue-labels"
        );

    const valuesElement =
        document.getElementById(
            "revenue-values"
        );


    if (!labelsElement || !valuesElement) {
        return;
    }


    let labels = [];
    let values = [];


    try {

        labels =
            JSON.parse(
                labelsElement.textContent
            );

        values =
            JSON.parse(
                valuesElement.textContent
            );

    } catch (error) {

        console.error(
            "Revenue chart data error:",
            error
        );

        return;

    }


    const ctx =
        canvas.getContext("2d");


    const gradient =
        ctx.createLinearGradient(
            0,
            0,
            0,
            260
        );


    gradient.addColorStop(
        0,
        "rgba(96, 165, 250, 0.20)"
    );

    gradient.addColorStop(
        1,
        "rgba(96, 165, 250, 0)"
    );


    new Chart(
        ctx,
        {

            type: "line",

            data: {

                labels: labels,

                datasets: [

                    {

                        label: "Revenue",

                        data: values,

                        borderColor:
                            "#60A5FA",

                        backgroundColor:
                            gradient,

                        fill: true,

                        borderWidth: 2,

                        tension: 0.4,

                        pointRadius: 0,

                        pointHoverRadius: 5,

                        pointBackgroundColor:
                            "#60A5FA",

                        pointBorderColor:
                            "#FFFFFF",

                        pointBorderWidth: 2

                    }

                ]

            },


            options: {

                responsive: true,

                maintainAspectRatio: false,


                interaction: {

                    intersect: false,

                    mode: "index"

                },


                plugins: {

                    legend: {

                        display: false

                    },


                    tooltip: {

                        backgroundColor:
                            "#141414",

                        titleColor:
                            "#F8FAFC",

                        bodyColor:
                            "#CBD5E1",

                        borderColor:
                            "rgba(148,163,184,0.12)",

                        borderWidth: 1,

                        padding: 10,

                        displayColors: false,

                        callbacks: {

                            label(context) {

                                const value =
                                    Number(
                                        context.raw || 0
                                    );

                                return (
                                    "Revenue: ৳" +
                                    value.toLocaleString(
                                        "en-BD"
                                    )
                                );

                            }

                        }

                    }

                },


                scales: {

                    x: {

                        grid: {

                            display: false

                        },

                        border: {

                            display: false

                        },

                        ticks: {

                            color:
                                "#64748B",

                            font: {

                                size: 9

                            },

                            maxRotation: 0,

                            autoSkip: true,

                            maxTicksLimit: 12

                        }

                    },


                    y: {

                        beginAtZero: true,

                        border: {

                            display: false

                        },

                        grid: {

                            color:
                                "rgba(148,163,184,0.06)"

                        },

                        ticks: {

                            color:
                                "#64748B",

                            font: {

                                size: 9

                            },

                            callback(value) {

                                if (
                                    value >= 100000
                                ) {

                                    return (
                                        "৳" +
                                        (
                                            value /
                                            100000
                                        ).toFixed(1) +
                                        "L"
                                    );

                                }


                                if (
                                    value >= 1000
                                ) {

                                    return (
                                        "৳" +
                                        (
                                            value /
                                            1000
                                        ).toFixed(0) +
                                        "K"
                                    );

                                }


                                return (
                                    "৳" +
                                    value
                                );

                            }

                        }

                    }

                },


                animation: {

                    duration: 1000,

                    easing:
                        "easeOutQuart"

                }

            }

        }
    );

}
/* =========================================================
   WINDOW RESIZE
========================================================= */

window.addEventListener("resize", () => {

    if (window.innerWidth > 992) {

        document
            .querySelector(".sidebar")
            ?.classList.remove("active");

    }

});

/* =========================================================
   REVENUE PERIOD SELECTOR
========================================================= */

function revenuePeriodSelector() {

    const selector =
        document.getElementById("revenuePeriod");

    if (!selector) return;

    selector.addEventListener(
        "change",
        function () {

            const selectedPeriod =
                this.value;

            const currentUrl =
                new URL(window.location.href);

            currentUrl.searchParams.set(
                "revenue_period",
                selectedPeriod
            );

            window.location.href =
                currentUrl.toString();

        }
    );

}

/* =========================================================
   END
========================================================= */