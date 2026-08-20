"use strict";

/* ======================================================
   GUIDELINE PLUGIN
====================================================== */

const guidelinePlugin = {
    id: "guideline",

    afterDraw(chart) {

        const tooltip = chart.tooltip;

        if (!tooltip || !tooltip._active || tooltip._active.length === 0) {
            return;
        }

        const ctx = chart.ctx;
        const x = tooltip._active[0].element.x;

        const top = chart.chartArea.top;
        const bottom = chart.chartArea.bottom;

        ctx.save();

        ctx.beginPath();

        ctx.setLineDash([6, 6]);

        ctx.moveTo(x, top);

        ctx.lineTo(x, bottom);

        ctx.lineWidth = 1;

        ctx.strokeStyle = "rgba(255,255,255,.25)";

        ctx.stroke();

        ctx.restore();

    }

};

Chart.register(guidelinePlugin);


/* ======================================================
   SALES CHART
====================================================== */

const salesCanvas = document.getElementById("salesChart");

if (salesCanvas) {

    const ctx = salesCanvas.getContext("2d");

    const gradient = ctx.createLinearGradient(0, 0, 0, 350);

    gradient.addColorStop(0, "rgba(34,197,94,.40)");
    gradient.addColorStop(.5, "rgba(34,197,94,.12)");
    gradient.addColorStop(1, "rgba(34,197,94,0)");

    new Chart(ctx, {

        type: "line",

        data: {

            labels: [

                "Jun",
                "Jul",
                "Aug",
                "Sep",
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

            ],

            datasets: [

                {

                    label: "Sales",

                    data: [

                        38000,
                        52000,
                        25000,
                        42000,
                        35000,
                        56000,
                        47000,
                        45151,
                        75892,
                        62521,
                        50100,
                        65050,
                        40000,
                        69500,
                        73000,
                        70500,
                    ],

                    borderColor: "#19db60",

                    backgroundColor: gradient,

                    fill: true,

                    borderWidth: 1.5,

                    tension: .45,

                    pointRadius: 0,

                    pointHoverRadius: 7,

                    pointBackgroundColor: "#22c55e",

                    pointBorderColor: "#ffffff",

                    pointBorderWidth: 3,

                    pointHoverBorderWidth: 3

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

                    backgroundColor: "#111827",

                    titleColor: "#ffffff",

                    bodyColor: "#ffffff",

                    displayColors: false,

                    padding: 14,

                    cornerRadius: 12,

                    callbacks: {

                        label(context) {

                            return "Sales : $" +
                                context.raw.toLocaleString();

                        }

                    }

                }

            },

            scales: {

                x: {

                    grid: {

                        display: false

                    },

                    ticks: {

                        color: "#94A3B8",

                        font: {

                            size: 13,

                            weight: 500

                        }

                    }

                },

                y: {

                    beginAtZero: true,

                    border: {

                        display: false

                    },

                    grid: {

                        color: "rgba(255,255,255,.05)",

                        drawTicks: false

                    },

                    ticks: {

                        stepSize: 10000,

                        color: "#94A3B8",

                        callback(value) {

                            return "$" + value / 1000 + "k";

                        }

                    }

                }

            },

            animation: {

                duration: 1800,

                easing: "easeOutQuart"

            }

        }

    });

}
/* ======================================================
   CENTER TEXT PLUGIN
====================================================== */

const centerTextPlugin = {

    id: "centerText",

    afterDraw(chart) {

        if (chart.config.type !== "doughnut") return;

        const {
            ctx,
            chartArea: { width, height }
        } = chart;

        const x = chart.getDatasetMeta(0).data[0].x;
        const y = chart.getDatasetMeta(0).data[0].y;

        ctx.save();

        ctx.textAlign = "center";

        ctx.fillStyle = "#94A3B8";
        ctx.font = "500 12px Poppins";

        ctx.fillText("Website", x, y - 16);

        ctx.fillStyle = "#FFFFFF";
        ctx.font = "600 21px Poppins";

        ctx.fillText("97.14%", x, y + 10);

        ctx.fillStyle = "#94A3B8";
        ctx.font = "500 12px Poppins";

        ctx.fillText("Growth", x, y + 34);

        ctx.restore();

    }

};

Chart.register(centerTextPlugin);



/* ======================================================
   VISITOR CHART
====================================================== */

const visitorCanvas = document.getElementById("visitorChart");

if (visitorCanvas) {

    new Chart(visitorCanvas, {

        type: "doughnut",

        data: {

            labels: [

                "Website",

                "Facebook",

                "Instagram",

                "WhatsApp"

            ],

            datasets: [

                {

                    data: [

                        55,

                        25,

                        12,

                        8

                    ],

                    backgroundColor: [

                        "#5B3DF5",

                        "#0EA5E9",

                        "#FACC15",

                        "#FB923C"

                    ],

                    borderWidth: 0,

                    borderRadius: 18,

                    spacing: 6,

                    hoverOffset: 12

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            radius: "80%",

            cutout: "90%",

            rotation: -90,

            plugins: {

                legend: {

                    position: "bottom",

                    labels: {

                        color: "#CBD5E1",

                        usePointStyle: true,

                        pointStyle: "circle",

                        padding: 18,

                        boxWidth: 10,

                        boxHeight: 10,

                        font: {

                            size: 13

                        }

                    }

                },

                tooltip: {

                    backgroundColor: "#111827",

                    titleColor: "#fff",

                    bodyColor: "#fff",

                    cornerRadius: 10,

                    padding: 10,

                    callbacks: {

                        label(context) {

                            return context.label + " : " + context.raw + "%";

                        }

                    }

                }

            },

            animation: {

                animateRotate: true,

                animateScale: true,

                duration: 1800,

                easing: "easeOutQuart"

            }

        }

    });

}




/* ======================================================
   GLOW EFFECT PLUGIN
====================================================== */

const glowLinePlugin = {

    id: "glowLine",

    beforeDatasetsDraw(chart) {

        if (chart.config.type !== "line") return;

        const ctx = chart.ctx;

        ctx.save();

        ctx.shadowColor = "rgba(34,197,94,.45)";
        ctx.shadowBlur = 18;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;

    },

    afterDatasetsDraw(chart) {

        if (chart.config.type !== "line") return;

        chart.ctx.restore();

    }

};


/* ======================================================
   ACTIVE POINT PLUGIN
====================================================== */

const activePointPlugin = {

    id: "activePoint",

    afterDatasetsDraw(chart) {

        if (chart.config.type !== "line") return;

        const tooltip = chart.tooltip;

        if (!tooltip || !tooltip._active || tooltip._active.length === 0) {
            return;
        }

        const point = tooltip._active[0].element;
        const ctx = chart.ctx;

        ctx.save();

        /* Outer Glow */

        ctx.beginPath();
        ctx.arc(point.x, point.y, 10, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(34,197,94,.18)";
        ctx.fill();

        /* White Ring */

        ctx.beginPath();
        ctx.arc(point.x, point.y, 6, 0, Math.PI * 2);
        ctx.fillStyle = "#FFFFFF";
        ctx.fill();

        /* Green Center */

        ctx.beginPath();
        ctx.arc(point.x, point.y, 3.5, 0, Math.PI * 2);
        ctx.fillStyle = "#22C55E";
        ctx.fill();

        ctx.restore();

    }

};

Chart.register(glowLinePlugin);
Chart.register(activePointPlugin);