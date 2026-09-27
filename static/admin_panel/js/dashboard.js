/* =========================================================
   NAFI ADMIN DASHBOARD
   Dashboard Interaction
   Demo Data Mode
========================================================= */

(function () {

    "use strict";


    /* =====================================================
       DASHBOARD DEMO DATA
    ===================================================== */

    const dashboardData = {

        totalSales: 125430,

        totalOrders: 328,

        netProfit: 32500,

        totalCustomers: 245,

        salesGrowth: 12.5,

        ordersGrowth: 8.3,

        profitGrowth: 15.2,

        customersGrowth: 10.4

    };


    /* =====================================================
       NUMBER FORMATTER
    ===================================================== */

    function formatNumber(number) {

        return Number(number).toLocaleString(
            "en-BD"
        );

    }


    /* =====================================================
       UPDATE OVERVIEW CARDS
    ===================================================== */

    function updateOverviewCards() {

        const sales =
            document.querySelector(
                "[data-dashboard-sales]"
            );


        const orders =
            document.querySelector(
                "[data-dashboard-orders]"
            );


        const profit =
            document.querySelector(
                "[data-dashboard-profit]"
            );


        const customers =
            document.querySelector(
                "[data-dashboard-customers]"
            );


        if (sales) {

            sales.textContent =
                "৳ " +
                formatNumber(
                    dashboardData.totalSales
                );

        }


        if (orders) {

            orders.textContent =
                formatNumber(
                    dashboardData.totalOrders
                );

        }


        if (profit) {

            profit.textContent =
                "৳ " +
                formatNumber(
                    dashboardData.netProfit
                );

        }


        if (customers) {

            customers.textContent =
                formatNumber(
                    dashboardData.totalCustomers
                );

        }

    }


    /* =====================================================
       PERIOD SWITCHER
    ===================================================== */

    function initializePeriodSwitcher() {

        const buttons =
            document.querySelectorAll(
                ".dashboard-period-btn"
            );


        if (!buttons.length) {
            return;
        }


        buttons.forEach(function (button) {

            button.addEventListener(
                "click",
                function () {

                    const period =
                        this.dataset.period;


                    if (!period) {
                        return;
                    }


                    buttons.forEach(
                        function (item) {

                            item.classList.remove(
                                "active"
                            );

                        }
                    );


                    this.classList.add(
                        "active"
                    );


                    /* ----------------------------------
                       UPDATE SALES CHART
                    ---------------------------------- */

                    if (
                        window.NAFIDashboardCharts
                    ) {

                        window
                            .NAFIDashboardCharts
                            .updateSalesChart(
                                period
                            );

                    }

                }
            );

        });

    }


    /* =====================================================
       TABLE ROW HOVER
    ===================================================== */

    function initializeTableInteraction() {

        const rows =
            document.querySelectorAll(
                ".dashboard-table tbody tr"
            );


        rows.forEach(function (row) {

            row.addEventListener(
                "mouseenter",
                function () {

                    this.classList.add(
                        "dashboard-row-active"
                    );

                }
            );


            row.addEventListener(
                "mouseleave",
                function () {

                    this.classList.remove(
                        "dashboard-row-active"
                    );

                }
            );

        });

    }


    /* =====================================================
       QUICK ACTION FEEDBACK
    ===================================================== */

    function initializeQuickActions() {

        const actions =
            document.querySelectorAll(
                ".dashboard-quick-action"
            );


        actions.forEach(function (action) {

            action.addEventListener(
                "click",
                function () {

                    /*
                     * Backend connection will be added later.
                     *
                     * For now we intentionally do not
                     * perform any dashboard action here.
                     */

                }
            );

        });

    }


    /* =====================================================
       DASHBOARD DATE
    ===================================================== */

    function initializeDashboardDate() {

        const dateElement =
            document.querySelector(
                "[data-dashboard-date]"
            );


        const timeElement =
            document.querySelector(
                "[data-dashboard-time]"
            );


        if (
            !dateElement &&
            !timeElement
        ) {

            return;

        }


        const now =
            new Date();


        const dateFormatter =
            new Intl.DateTimeFormat(
                "en-US",
                {

                    weekday: "long",

                    day: "2-digit",

                    month: "long",

                    year: "numeric"

                }
            );


        const timeFormatter =
            new Intl.DateTimeFormat(
                "en-US",
                {

                    hour: "2-digit",

                    minute: "2-digit",

                    hour12: true

                }
            );


        if (dateElement) {

            dateElement.textContent =
                dateFormatter.format(now);

        }


        if (timeElement) {

            timeElement.textContent =
                timeFormatter.format(now);

        }

    }


    /* =====================================================
       INITIALIZE DASHBOARD
    ===================================================== */

    function initializeDashboard() {

        updateOverviewCards();

        initializePeriodSwitcher();

        initializeTableInteraction();

        initializeQuickActions();

        initializeDashboardDate();

    }


    /* =====================================================
       DOM READY
    ===================================================== */

    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            initializeDashboard
        );

    } else {

        initializeDashboard();

    }


})();