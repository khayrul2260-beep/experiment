"use strict";

/* =========================================================
   NAFI ADMIN — CHART.JS
   Professional Chart Enhancements
========================================================= */


/* =========================================================
   GLOBAL CHART DEFAULTS
========================================================= */

if (typeof Chart !== "undefined") {

    Chart.defaults.font.family =
        "Poppins, sans-serif";

    Chart.defaults.color =
        "#94A3B8";

    Chart.defaults.animation.duration =
        900;

    Chart.defaults.animation.easing =
        "easeOutQuart";
}


/* =========================================================
   VERTICAL HOVER GUIDELINE
========================================================= */

const nafiGuidelinePlugin = {

    id: "nafiGuideline",

    afterDraw(chart) {

        const tooltip = chart.tooltip;

        if (
            !tooltip ||
            !tooltip._active ||
            tooltip._active.length === 0
        ) {
            return;
        }

        /*
         * Only apply to line charts.
         */
        if (chart.config.type !== "line") {
            return;
        }

        const activePoint =
            tooltip._active[0];

        if (!activePoint || !activePoint.element) {
            return;
        }

        const ctx = chart.ctx;

        const x =
            activePoint.element.x;

        const top =
            chart.chartArea.top;

        const bottom =
            chart.chartArea.bottom;

        ctx.save();

        ctx.beginPath();

        ctx.moveTo(x, top);
        ctx.lineTo(x, bottom);

        ctx.setLineDash([
            4,
            5
        ]);

        ctx.lineWidth = 1;

        ctx.strokeStyle =
            "rgba(148, 163, 184, 0.28)";

        ctx.stroke();

        ctx.restore();
    }
};


/* =========================================================
   ACTIVE DATA POINT
========================================================= */

const nafiActivePointPlugin = {

    id: "nafiActivePoint",

    afterDatasetsDraw(chart) {

        if (chart.config.type !== "line") {
            return;
        }

        const tooltip =
            chart.tooltip;

        if (
            !tooltip ||
            !tooltip._active ||
            tooltip._active.length === 0
        ) {
            return;
        }

        const active =
            tooltip._active[0];

        if (!active || !active.element) {
            return;
        }

        const point =
            active.element;

        const ctx =
            chart.ctx;

        ctx.save();


        /* -------------------------------------------------
           Soft outer glow
        ------------------------------------------------- */

        ctx.beginPath();

        ctx.arc(
            point.x,
            point.y,
            11,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            "rgba(37, 99, 235, 0.13)";

        ctx.fill();


        /* -------------------------------------------------
           White outer ring
        ------------------------------------------------- */

        ctx.beginPath();

        ctx.arc(
            point.x,
            point.y,
            6,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            "#FFFFFF";

        ctx.fill();


        /* -------------------------------------------------
           Blue center
        ------------------------------------------------- */

        ctx.beginPath();

        ctx.arc(
            point.x,
            point.y,
            3.2,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            "#2563EB";

        ctx.fill();


        ctx.restore();
    }
};


/* =========================================================
   SOFT LINE GLOW
========================================================= */

const nafiLineGlowPlugin = {

    id: "nafiLineGlow",

    beforeDatasetsDraw(chart) {

        if (chart.config.type !== "line") {
            return;
        }

        const ctx =
            chart.ctx;

        ctx.save();

        /*
         * Very subtle glow.
         *
         * Kept intentionally low so the
         * dashboard remains premium instead
         * of looking neon.
         */
        ctx.shadowColor =
            "rgba(37, 99, 235, 0.20)";

        ctx.shadowBlur = 10;

        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
    },


    afterDatasetsDraw(chart) {

        if (chart.config.type !== "line") {
            return;
        }

        chart.ctx.restore();
    }
};


/* =========================================================
   EMPTY CHART MESSAGE
========================================================= */

const nafiEmptyChartPlugin = {

    id: "nafiEmptyChart",

    afterDraw(chart) {

        if (
            !chart.data ||
            !chart.data.datasets ||
            !chart.data.datasets.length
        ) {
            drawEmptyMessage(chart);
            return;
        }

        const dataset =
            chart.data.datasets[0];

        if (
            !dataset ||
            !Array.isArray(dataset.data)
        ) {
            drawEmptyMessage(chart);
            return;
        }

        const hasData =
            dataset.data.some(
                value =>
                    Number(value) > 0
            );

        if (!hasData) {
            drawEmptyMessage(chart);
        }
    }
};


function drawEmptyMessage(chart) {

    const {
        ctx,
        chartArea
    } = chart;

    if (!chartArea) return;

    const centerX =
        (chartArea.left +
            chartArea.right) / 2;

    const centerY =
        (chartArea.top +
            chartArea.bottom) / 2;

    ctx.save();

    ctx.textAlign =
        "center";

    ctx.textBaseline =
        "middle";


    /* Main message */

    ctx.fillStyle =
        "#CBD5E1";

    ctx.font =
        "500 12px Poppins";

    ctx.fillText(
        "No revenue data available",
        centerX,
        centerY - 8
    );


    /* Secondary message */

    ctx.fillStyle =
        "#64748B";

    ctx.font =
        "400 9px Poppins";

    ctx.fillText(
        "Revenue will appear here after completed orders",
        centerX,
        centerY + 15
    );

    ctx.restore();
}


/* =========================================================
   DOUGHNUT CENTER TEXT HELPER
========================================================= */

const nafiDoughnutCenterPlugin = {

    id: "nafiDoughnutCenter",

    afterDraw(chart) {

        if (
            chart.config.type !== "doughnut"
        ) {
            return;
        }

        /*
         * Only draw if custom center
         * values have been supplied.
         */
        const centerTitle =
            chart.options.plugins
                ?.nafiDoughnutCenter
                ?.title;

        const centerValue =
            chart.options.plugins
                ?.nafiDoughnutCenter
                ?.value;

        const centerSubtitle =
            chart.options.plugins
                ?.nafiDoughnutCenter
                ?.subtitle;

        if (
            centerTitle === undefined &&
            centerValue === undefined &&
            centerSubtitle === undefined
        ) {
            return;
        }

        const meta =
            chart.getDatasetMeta(0);

        if (
            !meta ||
            !meta.data ||
            !meta.data.length
        ) {
            return;
        }

        const point =
            meta.data[0];

        const x =
            point.x;

        const y =
            point.y;

        const ctx =
            chart.ctx;

        ctx.save();

        ctx.textAlign =
            "center";

        ctx.textBaseline =
            "middle";


        /* -------------------------------------------------
           Title
        ------------------------------------------------- */

        if (centerTitle) {

            ctx.fillStyle =
                "#94A3B8";

            ctx.font =
                "500 10px Poppins";

            ctx.fillText(
                centerTitle,
                x,
                y - 23
            );
        }


        /* -------------------------------------------------
           Main value
        ------------------------------------------------- */

        if (centerValue) {

            ctx.fillStyle =
                "#F8FAFC";

            ctx.font =
                "600 20px Poppins";

            ctx.fillText(
                centerValue,
                x,
                y + 1
            );
        }


        /* -------------------------------------------------
           Subtitle
        ------------------------------------------------- */

        if (centerSubtitle) {

            ctx.fillStyle =
                "#64748B";

            ctx.font =
                "400 9px Poppins";

            ctx.fillText(
                centerSubtitle,
                x,
                y + 23
            );
        }

        ctx.restore();
    }
};


/* =========================================================
   PROFESSIONAL TOOLTIP HELPERS
========================================================= */

function nafiCurrencyTooltipLabel(context) {

    const value =
        Number(context.raw) || 0;

    return (
        "Revenue: ৳" +
        value.toLocaleString(
            "en-US"
        )
    );
}


/* =========================================================
   CHART UTILITIES
========================================================= */

function nafiFormatCurrency(value) {

    const number =
        Number(value) || 0;

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


    return (
        "৳" +
        number.toLocaleString(
            "en-US"
        )
    );
}


/* =========================================================
   REGISTER PLUGINS
========================================================= */

if (typeof Chart !== "undefined") {

    Chart.register(
        nafiGuidelinePlugin,
        nafiActivePointPlugin,
        nafiLineGlowPlugin,
        nafiEmptyChartPlugin,
        nafiDoughnutCenterPlugin
    );
}


/* =========================================================
   CHART INSTANCE CLEANUP
========================================================= */

function nafiDestroyChart(canvas) {

    if (
        typeof Chart === "undefined" ||
        !canvas
    ) {
        return;
    }

    const existing =
        Chart.getChart(canvas);

    if (existing) {
        existing.destroy();
    }
}


/* =========================================================
   SAFE CHART RESIZE
========================================================= */

function nafiResizeCharts() {

    if (typeof Chart === "undefined") {
        return;
    }

    Chart.instances &&
        Object.values(
            Chart.instances
        ).forEach((chart) => {

            if (chart) {
                chart.resize();
            }
        });
}


/* =========================================================
   WINDOW RESIZE
========================================================= */

let nafiChartResizeTimer = null;

window.addEventListener(
    "resize",
    () => {

        clearTimeout(
            nafiChartResizeTimer
        );

        nafiChartResizeTimer =
            setTimeout(() => {

                nafiResizeCharts();

            }, 180);
    }
);


/* =========================================================
   PUBLIC HELPERS
========================================================= */

window.NAFICharts = {

    formatCurrency:
        nafiFormatCurrency,

    currencyTooltip:
        nafiCurrencyTooltipLabel,

    destroy:
        nafiDestroyChart,

    resize:
        nafiResizeCharts
};


/* =========================================================
   END OF CHART.JS
========================================================= */