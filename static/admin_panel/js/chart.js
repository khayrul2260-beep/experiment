/* ============================================================
   NAFI ADMIN DASHBOARD
   chart.js
   Chart.js 4.x compatible
   ============================================================ */

(function () {

    "use strict";


    /* ========================================================
       GLOBAL CHART STORAGE
    ======================================================== */

    const NAFI_CHARTS = {};


    /* ========================================================
       DOM READY
    ======================================================== */

    document.addEventListener("DOMContentLoaded", function () {

        initializeRevenueChart();

    });


    /* ========================================================
       REVENUE CHART
    ======================================================== */

    function initializeRevenueChart() {

        const canvas =
            document.getElementById(
                "revenueChart"
            );


        if (!canvas) {
            return;
        }


        /*
         * Destroy an existing chart if the page/component
         * is initialized again.
         */

        destroyChart("revenueChart");


        const labels =
            parseChartData(
                canvas.dataset.labels
            );


        const values =
            parseChartData(
                canvas.dataset.values
            );


        /*
         * If Django has no revenue data, show an empty
         * but valid chart instead of throwing an error.
         */

        const safeLabels =
            Array.isArray(labels)
                ? labels
                : [];


        const safeValues =
            Array.isArray(values)
                ? values
                : [];


        const context =
            canvas.getContext("2d");


        if (!context) {
            return;
        }


        /* ====================================================
           GRADIENT
        ==================================================== */

        const chartHeight =
            canvas.parentElement
                ? canvas.parentElement.clientHeight
                : 250;


        const gradient =
            context.createLinearGradient(
                0,
                0,
                0,
                chartHeight
            );


        gradient.addColorStop(
            0,
            "rgba(77, 141, 255, 0.20)"
        );


        gradient.addColorStop(
            0.65,
            "rgba(77, 141, 255, 0.045)"
        );


        gradient.addColorStop(
            1,
            "rgba(77, 141, 255, 0)"
        );


        /* ====================================================
           CHART CONFIGURATION
        ==================================================== */

        const config = {

            type: "line",

            data: {

                labels: safeLabels,

                datasets: [

                    {

                        label: "Revenue",

                        data: safeValues,

                        borderColor:
                            "#4d8dff",

                        backgroundColor:
                            gradient,

                        borderWidth: 2,

                        fill: true,

                        tension: 0.38,

                        cubicInterpolationMode:
                            "monotone",

                        pointRadius: 0,

                        pointHoverRadius: 5,

                        pointHoverBorderWidth: 2,

                        pointBackgroundColor:
                            "#4d8dff",

                        pointBorderColor:
                            "#050505",

                        pointHoverBackgroundColor:
                            "#4d8dff",

                        pointHoverBorderColor:
                            "#f5f7fa",

                    }

                ]

            },


            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: {

                    duration: 650,

                    easing: "easeOutQuart"

                },


                interaction: {

                    mode: "index",

                    intersect: false

                },


                layout: {

                    padding: {

                        top: 5,

                        right: 8,

                        bottom: 2,

                        left: 0

                    }

                },


                plugins: {

                    legend: {

                        display: false

                    },


                    title: {

                        display: false

                    },


                    tooltip: {

                        enabled: true,

                        backgroundColor:
                            "rgba(12, 12, 12, 0.96)",

                        borderColor:
                            "rgba(77, 141, 255, 0.28)",

                        borderWidth: 1,

                        titleColor:
                            "#969ca7",

                        bodyColor:
                            "#f5f7fa",

                        titleFont: {

                            family:
                                "Poppins, Inter, sans-serif",

                            size: 8,

                            weight: "500"

                        },

                        bodyFont: {

                            family:
                                "Poppins, Inter, sans-serif",

                            size: 10,

                            weight: "600"

                        },

                        padding: 9,

                        cornerRadius: 7,

                        displayColors: false,

                        callbacks: {

                            label: function (context) {

                                const value =
                                    Number(
                                        context.raw || 0
                                    );


                                return (
                                    "৳" +
                                    formatNumber(value)
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
                                "#777d87",

                            font: {

                                family:
                                    "Poppins, Inter, sans-serif",

                                size: 7,

                                weight: "400"

                            },

                            padding: 7,

                            maxRotation: 0,

                            autoSkip: true,

                            autoSkipPadding: 15

                        }

                    },


                    y: {

                        beginAtZero: true,

                        border: {

                            display: false,

                            dash: [3, 4]

                        },

                        grid: {

                            color:
                                "rgba(255,255,255,0.045)",

                            drawTicks: false,

                            lineWidth: 1

                        },

                        ticks: {

                            color:
                                "#777d87",

                            font: {

                                family:
                                    "Poppins, Inter, sans-serif",

                                size: 7,

                                weight: "400"

                            },

                            padding: 8,

                            maxTicksLimit: 5,

                            callback: function (value) {

                                return formatAxisValue(
                                    value
                                );

                            }

                        }

                    }

                }

            }

        };


        /*
         * Create chart.
         */

        NAFI_CHARTS.revenueChart =
            new Chart(
                context,
                config
            );


        /*
         * Store chart on canvas as well.
         * Useful for debugging and controlled updates.
         */

        canvas._nafiChart =
            NAFI_CHARTS.revenueChart;


        /*
         * Add vertical hover guideline.
         */

        attachHoverGuideline(
            canvas,
            NAFI_CHARTS.revenueChart
        );

    }


    /* ========================================================
       DATA PARSER
    ======================================================== */

    function parseChartData(value) {

        if (!value) {
            return [];
        }


        /*
         * Normal JSON
         */

        try {

            return JSON.parse(value);

        } catch (error) {

            /*
             * Django's default Python list representation may
             * use single quotes.
             *
             * Example:
             *
             * ['Jan', 'Feb', 'Mar']
             *
             * Convert the simple dashboard representation
             * into valid JSON.
             */

            try {

                const normalized =
                    value
                        .replace(
                            /'/g,
                            '"'
                        );


                return JSON.parse(
                    normalized
                );

            } catch (secondError) {

                console.warn(
                    "NAFI Chart: Unable to parse chart data.",
                    secondError
                );

                return [];

            }

        }

    }


    /* ========================================================
       NUMBER FORMAT
    ======================================================== */

    function formatNumber(value) {

        const number =
            Number(value);


        if (!Number.isFinite(number)) {

            return "0";

        }


        return number.toLocaleString(
            "en-BD",
            {
                maximumFractionDigits: 0
            }
        );

    }


    /* ========================================================
       Y AXIS FORMAT
    ======================================================== */

    function formatAxisValue(value) {

        const number =
            Number(value);


        if (!Number.isFinite(number)) {

            return "৳0";

        }


        if (number >= 1000000) {

            return (
                "৳" +
                (number / 1000000)
                    .toFixed(
                        number % 1000000 === 0
                            ? 0
                            : 1
                    ) +
                "M"
            );

        }


        if (number >= 1000) {

            return (
                "৳" +
                (number / 1000)
                    .toFixed(
                        number % 1000 === 0
                            ? 0
                            : 1
                    ) +
                "K"
            );

        }


        return "৳" + number;

    }


    /* ========================================================
       HOVER GUIDELINE PLUGIN
    ======================================================== */

    function attachHoverGuideline(
        canvas,
        chart
    ) {

        if (!chart) {
            return;
        }


        const guidelinePlugin = {

            id: "nafiHoverGuideline",


            afterDraw: function (
                currentChart
            ) {

                const tooltip =
                    currentChart.tooltip;


                if (
                    !tooltip ||
                    !tooltip.getActiveElements ||
                    !tooltip.getActiveElements().length
                ) {

                    return;

                }


                const active =
                    tooltip.getActiveElements()[0];


                if (!active) {
                    return;
                }


                const x =
                    active.element.x;


                const chartArea =
                    currentChart.chartArea;


                if (!chartArea) {
                    return;
                }


                const ctx =
                    currentChart.ctx;


                ctx.save();


                ctx.beginPath();


                ctx.moveTo(
                    x,
                    chartArea.top
                );


                ctx.lineTo(
                    x,
                    chartArea.bottom
                );


                ctx.lineWidth = 1;


                ctx.setLineDash([
                    3,
                    4
                ]);


                ctx.strokeStyle =
                    "rgba(77, 141, 255, 0.22)";


                ctx.stroke();


                ctx.restore();

            }

        };


        /*
         * Register only once for this chart.
         */

        chart.config.plugins =
            chart.config.plugins || [];


        chart.config.plugins.push(
            guidelinePlugin
        );


        chart.update(
            "none"
        );

    }


    /* ========================================================
       DESTROY CHART
    ======================================================== */

    function destroyChart(
        chartName
    ) {

        const chart =
            NAFI_CHARTS[chartName];


        if (!chart) {
            return;
        }


        try {

            chart.destroy();

        } catch (error) {

            console.warn(
                "NAFI Chart destroy error:",
                error
            );

        }


        delete NAFI_CHARTS[chartName];

    }


    /* ========================================================
       RESIZE CHART
    ======================================================== */

    function resizeCharts() {

        Object.keys(
            NAFI_CHARTS
        ).forEach(function (key) {

            const chart =
                NAFI_CHARTS[key];


            if (
                chart &&
                typeof chart.resize === "function"
            ) {

                chart.resize();

            }

        });

    }


    /* ========================================================
       WINDOW RESIZE
    ======================================================== */

    let resizeTimer = null;


    window.addEventListener(
        "resize",
        function () {

            clearTimeout(
                resizeTimer
            );


            resizeTimer =
                setTimeout(
                    function () {

                        resizeCharts();

                    },
                    150
                );

        }
    );


    /* ========================================================
       PUBLIC CHART API
    ======================================================== */

    window.NAFICharts = {

        get: function (
            chartName
        ) {

            return NAFI_CHARTS[
                chartName
            ] || null;

        },


        destroy: function (
            chartName
        ) {

            destroyChart(
                chartName
            );

        },


        resize: function () {

            resizeCharts();

        },


        revenue: function () {

            return NAFI_CHARTS.revenueChart || null;

        }

    };


})();