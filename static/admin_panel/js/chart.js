/* =========================================================
   NAFI ADMIN DASHBOARD
   DEMO CHART DATA
   Frontend only — No Backend Connection
========================================================= */

(function () {

    "use strict";


    /* =====================================================
       DEMO DATA
    ===================================================== */

    const dashboardChartData = {

        /* -------------------------------------------------
           SALES OVERVIEW
        ------------------------------------------------- */

        sales: {

            "7 Days": {
                labels: [
                    "Sep 20",
                    "Sep 21",
                    "Sep 22",
                    "Sep 23",
                    "Sep 24",
                    "Sep 25",
                    "Sep 26"
                ],

                values: [
                    6200,
                    8400,
                    7100,
                    9800,
                    8900,
                    11200,
                    12800
                ]
            },


            "30 Days": {
                labels: [
                    "Aug 28",
                    "Aug 30",
                    "Sep 2",
                    "Sep 5",
                    "Sep 8",
                    "Sep 11",
                    "Sep 14",
                    "Sep 17",
                    "Sep 20",
                    "Sep 23",
                    "Sep 26"
                ],

                values: [
                    5200,
                    7600,
                    6800,
                    9400,
                    12100,
                    10800,
                    14700,
                    13200,
                    17800,
                    21500,
                    24800
                ]
            },


            "3 Months": {
                labels: [
                    "Jul",
                    "Jul 10",
                    "Jul 20",
                    "Jul 30",
                    "Aug 10",
                    "Aug 20",
                    "Aug 30",
                    "Sep 10",
                    "Sep 20",
                    "Sep 26"
                ],

                values: [
                    8400,
                    11200,
                    9800,
                    13500,
                    14800,
                    17200,
                    19400,
                    21800,
                    23600,
                    24800
                ]
            },


            "1 Year": {
                labels: [
                    "Oct",
                    "Nov",
                    "Dec",
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep"
                ],

                values: [
                    78000,
                    85000,
                    92000,
                    88000,
                    104000,
                    112000,
                    118000,
                    125000,
                    132000,
                    141000,
                    151000,
                    158000
                ]
            }

        },


        /* -------------------------------------------------
           REVENUE / EXPENSE / PROFIT
        ------------------------------------------------- */

        financial: {

            labels: [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun"
            ],

            revenue: [
                102000,
                126000,
                134000,
                151000,
                168000,
                182000
            ],

            expense: [
                51000,
                68000,
                72000,
                83000,
                91000,
                96000
            ],

            profit: [
                51000,
                58000,
                62000,
                68000,
                77000,
                86000
            ]

        },


        /* -------------------------------------------------
           SALES BY CATEGORY
        ------------------------------------------------- */

        categories: {

            labels: [
                "T-Shirts",
                "Punjabi",
                "Shirts",
                "Polo",
                "Hoodies",
                "Others"
            ],

            values: [
                38,
                22,
                16,
                12,
                8,
                4
            ]

        }

    };


    /* =====================================================
       GLOBAL CHART SETTINGS
    ===================================================== */

    Chart.defaults.font.family =
        "Manrope, Arial, sans-serif";

    Chart.defaults.font.size = 9;

    Chart.defaults.color = "#777777";

    Chart.defaults.animation.duration = 700;


    /* =====================================================
       COMMON OPTIONS
    ===================================================== */

    const commonGrid = {

        color: "rgba(255,255,255,0.055)",

        drawBorder: false

    };


    /* =====================================================
       SALES OVERVIEW CHART
    ===================================================== */

    let salesChart = null;


    function createSalesChart(period = "30 Days") {

        const canvas =
            document.getElementById("salesOverviewChart");

        if (!canvas) {
            return;
        }


        const data =
            dashboardChartData.sales[period];


        if (!data) {
            return;
        }


        if (salesChart) {
            salesChart.destroy();
        }


        const ctx = canvas.getContext("2d");


        /* -----------------------------------------------
           Gradient
        ------------------------------------------------ */

        const gradient =
            ctx.createLinearGradient(
                0,
                0,
                0,
                300
            );

        gradient.addColorStop(
            0,
            "rgba(255,255,255,0.16)"
        );

        gradient.addColorStop(
            1,
            "rgba(255,255,255,0)"
        );


        salesChart = new Chart(ctx, {

            type: "line",

            data: {

                labels: data.labels,

                datasets: [{

                    label: "Sales",

                    data: data.values,

                    borderColor: "#f1f1f1",

                    backgroundColor: gradient,

                    borderWidth: 1.5,

                    fill: true,

                    tension: 0.38,

                    pointRadius: 2.5,

                    pointHoverRadius: 5,

                    pointBackgroundColor: "#f1f1f1",

                    pointBorderColor: "#080808",

                    pointBorderWidth: 2

                }]

            },


            options: {

                responsive: true,

                maintainAspectRatio: false,

                interaction: {

                    mode: "index",

                    intersect: false

                },


                plugins: {

                    legend: {

                        display: false

                    },


                    tooltip: {

                        backgroundColor: "#151515",

                        borderColor: "#303030",

                        borderWidth: 1,

                        titleColor: "#ffffff",

                        bodyColor: "#cccccc",

                        padding: 10,

                        displayColors: false,

                        callbacks: {

                            label: function (context) {

                                return (
                                    "Sales: ৳ " +
                                    Number(
                                        context.raw
                                    ).toLocaleString(
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

                            color: "#666666",

                            maxRotation: 0,

                            autoSkip: true,

                            maxTicksLimit: 8,

                            font: {

                                size: 8

                            }

                        }

                    },


                    y: {

                        beginAtZero: true,

                        grid: commonGrid,

                        border: {

                            display: false

                        },

                        ticks: {

                            color: "#666666",

                            font: {

                                size: 8

                            },

                            callback: function (value) {

                                if (
                                    value >= 1000
                                ) {

                                    return (
                                        "৳" +
                                        (
                                            value /
                                            1000
                                        ) +
                                        "k"
                                    );

                                }

                                return "৳" + value;

                            }

                        }

                    }

                }

            }

        });

    }


    /* =====================================================
       REVENUE / EXPENSE / PROFIT CHART
    ===================================================== */

    let financialChart = null;


    function createFinancialChart() {

        const canvas =
            document.getElementById(
                "revenueExpenseChart"
            );


        if (!canvas) {
            return;
        }


        if (financialChart) {
            financialChart.destroy();
        }


        financialChart = new Chart(
            canvas.getContext("2d"),
            {

                type: "bar",

                data: {

                    labels:
                        dashboardChartData.financial.labels,

                    datasets: [

                        {

                            label: "Revenue",

                            data:
                                dashboardChartData
                                    .financial
                                    .revenue,

                            backgroundColor:
                                "#d8d8d8",

                            borderRadius: 2,

                            barPercentage: 0.72,

                            categoryPercentage: 0.62

                        },


                        {

                            label: "Expenses",

                            data:
                                dashboardChartData
                                    .financial
                                    .expense,

                            backgroundColor:
                                "#777777",

                            borderRadius: 2,

                            barPercentage: 0.72,

                            categoryPercentage: 0.62

                        },


                        {

                            label: "Profit",

                            data:
                                dashboardChartData
                                    .financial
                                    .profit,

                            backgroundColor:
                                "#f1f1f1",

                            borderRadius: 2,

                            barPercentage: 0.72,

                            categoryPercentage: 0.62

                        }

                    ]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,


                    plugins: {

                        legend: {

                            display: false

                        },


                        tooltip: {

                            backgroundColor: "#151515",

                            borderColor: "#303030",

                            borderWidth: 1,

                            titleColor: "#ffffff",

                            bodyColor: "#cccccc",

                            padding: 9,

                            callbacks: {

                                label: function (
                                    context
                                ) {

                                    return (
                                        context.dataset.label +
                                        ": ৳ " +
                                        Number(
                                            context.raw
                                        ).toLocaleString(
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

                                color: "#666666",

                                font: {

                                    size: 8

                                }

                            }

                        },


                        y: {

                            beginAtZero: true,

                            grid: commonGrid,

                            border: {

                                display: false

                            },

                            ticks: {

                                color: "#666666",

                                font: {

                                    size: 8

                                },

                                callback: function (
                                    value
                                ) {

                                    return (
                                        "৳" +
                                        (
                                            value /
                                            1000
                                        ) +
                                        "k"
                                    );

                                }

                            }

                        }

                    }

                }

            }

        );

    }


    /* =====================================================
       CATEGORY DOUGHNUT
    ===================================================== */

    let categoryChart = null;


    function createCategoryChart() {

        const canvas =
            document.getElementById(
                "categorySalesChart"
            );


        if (!canvas) {
            return;
        }


        if (categoryChart) {
            categoryChart.destroy();
        }


        categoryChart = new Chart(
            canvas.getContext("2d"),
            {

                type: "doughnut",

                data: {

                    labels:
                        dashboardChartData
                            .categories
                            .labels,

                    datasets: [{

                        data:
                            dashboardChartData
                                .categories
                                .values,

                        backgroundColor: [

                            "#eeeeee",

                            "#bdbdbd",

                            "#969696",

                            "#777777",

                            "#5d5d5d",

                            "#3f3f3f"

                        ],

                        borderColor:
                            "#0d0d0d",

                        borderWidth: 2,

                        hoverOffset: 3

                    }]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "66%",


                    plugins: {

                        legend: {

                            display: false

                        },


                        tooltip: {

                            backgroundColor:
                                "#151515",

                            borderColor:
                                "#303030",

                            borderWidth: 1,

                            titleColor:
                                "#ffffff",

                            bodyColor:
                                "#cccccc",

                            padding: 9,

                            callbacks: {

                                label: function (
                                    context
                                ) {

                                    return (
                                        context.label +
                                        ": " +
                                        context.raw +
                                        "%"
                                    );

                                }

                            }

                        }

                    }

                }

            }

        );

    }


    /* =====================================================
       INITIALIZE ALL CHARTS
    ===================================================== */

    function initializeDashboardCharts() {

        if (
            typeof Chart ===
            "undefined"
        ) {

            console.warn(
                "Chart.js is not loaded."
            );

            return;

        }


        createSalesChart("30 Days");

        createFinancialChart();

        createCategoryChart();

    }


    /* =====================================================
       PUBLIC API
    ===================================================== */

    window.NAFIDashboardCharts = {

        updateSalesChart:
            createSalesChart,

        refresh:
            initializeDashboardCharts

    };


    /* =====================================================
       DOM READY
    ===================================================== */

    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            initializeDashboardCharts
        );

    } else {

        initializeDashboardCharts();

    }


})();