document.addEventListener("DOMContentLoaded", () => {
    "use strict";


    /* =========================================================
       ELEMENTS
    ========================================================= */

    const couponForm =
        document.getElementById("coupon-form");

    const couponInput =
        document.getElementById("coupon-code");

    const couponApplyButton =
        document.getElementById("coupon-apply-btn");

    const couponApplied =
        document.getElementById("coupon-applied");

    const couponAppliedCode =
        document.getElementById("coupon-applied-code");

    const couponRemoveButton =
        document.getElementById("coupon-remove-btn");

    const couponMessage =
        document.getElementById("coupon-message");


    const subtotalElement =
        document.getElementById("checkout-subtotal");

    const discountElement =
        document.getElementById("checkout-discount");

    const discountRow =
        document.getElementById("checkout-discount-row");

    const deliveryElement =
        document.getElementById("checkout-delivery");

    const totalElement =
        document.getElementById("checkout-total");


    const checkoutForm =
        document.getElementById("checkout-form");

    const placeOrderButton =
        document.getElementById("place-order-btn");


    /* =========================================================
       CSRF TOKEN
    ========================================================= */

    function getCSRFToken() {

        const csrfInput =
            document.querySelector(
                'input[name="csrfmiddlewaretoken"]'
            );


        if (
            csrfInput &&
            csrfInput.value
        ) {

            return csrfInput.value;

        }


        const cookie =
            document.cookie
                .split("; ")
                .find(
                    row =>
                        row.startsWith("csrftoken=")
                );


        if (!cookie) {

            return "";

        }


        return decodeURIComponent(
            cookie.split("=")[1]
        );

    }


    /* =========================================================
       MONEY FORMAT
    ========================================================= */

    function formatMoney(value) {

        const number =
            Number(value || 0);


        return number.toFixed(2);

    }


    /* =========================================================
       COUPON MESSAGE
    ========================================================= */

    function showCouponMessage(
        message,
        type = "error"
    ) {

        if (!couponMessage) {

            return;

        }


        couponMessage.textContent =
            message || "";


        couponMessage.classList.remove(
            "show",
            "success",
            "error"
        );


        if (type === "success") {

            couponMessage.classList.add(
                "success"
            );

        } else {

            couponMessage.classList.add(
                "error"
            );

        }


        couponMessage.classList.add(
            "show"
        );

    }


    function hideCouponMessage() {

        if (!couponMessage) {

            return;

        }


        couponMessage.textContent = "";


        couponMessage.classList.remove(
            "show",
            "success",
            "error"
        );

    }


    /* =========================================================
       UPDATE ORDER SUMMARY
    ========================================================= */

    function updateSummary(data) {

        if (
            subtotalElement &&
            data.subtotal !== undefined
        ) {

            subtotalElement.textContent =
                formatMoney(
                    data.subtotal
                );

        }


        if (
            discountElement &&
            data.discount !== undefined
        ) {

            const discount =
                Number(
                    data.discount || 0
                );


            discountElement.textContent =
                formatMoney(
                    discount
                );


            if (discountRow) {

                if (discount > 0) {

                    discountRow.style.display =
                        "";

                } else {

                    discountRow.style.display =
                        "none";

                }

            }

        }


        if (
            deliveryElement &&
            data.delivery_charge !== undefined
        ) {

            deliveryElement.textContent =
                formatMoney(
                    data.delivery_charge
                );

        }


        if (
            totalElement &&
            data.total_amount !== undefined
        ) {

            totalElement.textContent =
                formatMoney(
                    data.total_amount
                );

        }

    }


    /* =========================================================
       SHOW APPLIED COUPON
    ========================================================= */

    function showAppliedCoupon(code) {

        if (couponAppliedCode) {

            couponAppliedCode.textContent =
                code || "";

        }


        if (couponForm) {

            couponForm.classList.add(
                "coupon-hidden"
            );

        }


        if (couponApplied) {

            couponApplied.classList.remove(
                "coupon-hidden"
            );

        }

    }


    /* =========================================================
       SHOW COUPON FORM
    ========================================================= */

    function showCouponForm() {

        if (couponApplied) {

            couponApplied.classList.add(
                "coupon-hidden"
            );

        }


        if (couponForm) {

            couponForm.classList.remove(
                "coupon-hidden"
            );

        }

    }


    /* =========================================================
       APPLY BUTTON LOADING
    ========================================================= */

    function setApplyLoading(
        isLoading
    ) {

        if (!couponApplyButton) {

            return;

        }


        if (isLoading) {

            if (
                !couponApplyButton.dataset.originalText
            ) {

                couponApplyButton.dataset.originalText =
                    couponApplyButton.textContent;

            }


            couponApplyButton.disabled =
                true;


            couponApplyButton.textContent =
                "APPLYING...";

        } else {

            couponApplyButton.disabled =
                false;


            couponApplyButton.textContent =
                couponApplyButton.dataset.originalText ||
                "APPLY";

        }

    }


    /* =========================================================
       REMOVE BUTTON LOADING
    ========================================================= */

    function setRemoveLoading(
        isLoading
    ) {

        if (!couponRemoveButton) {

            return;

        }


        if (isLoading) {

            if (
                !couponRemoveButton.dataset.originalText
            ) {

                couponRemoveButton.dataset.originalText =
                    couponRemoveButton.textContent;

            }


            couponRemoveButton.disabled =
                true;


            couponRemoveButton.textContent =
                "REMOVING...";

        } else {

            couponRemoveButton.disabled =
                false;


            couponRemoveButton.textContent =
                couponRemoveButton.dataset.originalText ||
                "REMOVE";

        }

    }


    /* =========================================================
       SERVER POST REQUEST
    ========================================================= */

    async function sendPostRequest(
        url,
        data = {}
    ) {

        if (!url) {

            throw new Error(
                "Request URL is missing."
            );

        }


        const response =
            await fetch(
                url,
                {
                    method: "POST",

                    headers: {
                        "X-CSRFToken":
                            getCSRFToken(),

                        "X-Requested-With":
                            "XMLHttpRequest",

                        "Content-Type":
                            "application/x-www-form-urlencoded; charset=UTF-8"
                    },

                    body:
                        new URLSearchParams(
                            data
                        )
                }
            );


        let result;


        try {

            result =
                await response.json();

        } catch (error) {

            throw new Error(
                "Invalid server response."
            );

        }


        return {
            response,
            data: result
        };

    }


    /* =========================================================
       APPLY COUPON
    ========================================================= */

    if (couponForm) {

        couponForm.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();


                const code =
                    couponInput
                        ? couponInput.value.trim()
                        : "";


                hideCouponMessage();


                /* -----------------------------------------
                   EMPTY CODE
                ----------------------------------------- */

                if (!code) {

                    showCouponMessage(
                        "Please enter a coupon code.",
                        "error"
                    );


                    if (couponInput) {

                        couponInput.focus();

                    }


                    return;

                }


                setApplyLoading(true);


                try {

                    const {
                        response,
                        data
                    } =
                        await sendPostRequest(
                            couponForm.action,
                            {
                                code: code
                            }
                        );


                    /* -------------------------------------
                       INVALID COUPON
                    ------------------------------------- */

                    if (
                        !response.ok ||
                        !data.success
                    ) {

                        if (
                            data.subtotal !==
                            undefined
                        ) {

                            updateSummary({

                                subtotal:
                                    data.subtotal,

                                discount:
                                    "0.00",

                                delivery_charge:
                                    data.delivery_charge ||
                                    "0.00",

                                total_amount:
                                    data.total_amount ||
                                    data.subtotal ||
                                    "0.00"

                            });

                        }


                        showCouponForm();


                        showCouponMessage(
                            data.message ||
                            "This coupon could not be applied.",
                            "error"
                        );


                        return;

                    }


                    /* -------------------------------------
                       VALID COUPON
                    ------------------------------------- */

                    updateSummary(data);


                    showAppliedCoupon(
                        data.coupon_code ||
                        code
                    );


                    showCouponMessage(
                        data.message ||
                        "Coupon applied successfully.",
                        "success"
                    );


                    if (couponInput) {

                        couponInput.value =
                            "";

                    }

                } catch (error) {

                    console.error(
                        "NAFI: Apply coupon error:",
                        error
                    );


                    showCouponMessage(
                        "Something went wrong. Please try again.",
                        "error"
                    );

                } finally {

                    setApplyLoading(
                        false
                    );

                }

            }
        );

    }


    /* =========================================================
       REMOVE COUPON
    ========================================================= */

    if (couponRemoveButton) {

        couponRemoveButton.addEventListener(
            "click",
            async () => {

                hideCouponMessage();


                const removeUrl =
                    couponRemoveButton.dataset.url;


                if (!removeUrl) {

                    showCouponMessage(
                        "Coupon removal URL is missing.",
                        "error"
                    );


                    return;

                }


                setRemoveLoading(true);


                try {

                    const {
                        response,
                        data
                    } =
                        await sendPostRequest(
                            removeUrl
                        );


                    /* -------------------------------------
                       REMOVE FAILED
                    ------------------------------------- */

                    if (
                        !response.ok ||
                        !data.success
                    ) {

                        showCouponMessage(
                            data.message ||
                            "Unable to remove coupon.",
                            "error"
                        );


                        return;

                    }


                    /* -------------------------------------
                       REMOVE SUCCESS
                    ------------------------------------- */

                    updateSummary(data);


                    showCouponForm();


                    if (couponInput) {

                        couponInput.value =
                            "";

                    }


                    showCouponMessage(
                        data.message ||
                        "Coupon removed successfully.",
                        "success"
                    );

                } catch (error) {

                    console.error(
                        "NAFI: Remove coupon error:",
                        error
                    );


                    showCouponMessage(
                        "Something went wrong. Please try again.",
                        "error"
                    );

                } finally {

                    setRemoveLoading(
                        false
                    );

                }

            }
        );

    }


    /* =========================================================
       COUPON INPUT — UPPERCASE
    ========================================================= */

    if (couponInput) {

        couponInput.addEventListener(
            "input",
            () => {

                couponInput.value =
                    couponInput.value.toUpperCase();

            }
        );

    }


    /* =========================================================
       COUPON INPUT — ENTER KEY
    ========================================================= */

    if (couponInput) {

        couponInput.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key !== "Enter"
                ) {

                    return;

                }


                event.preventDefault();


                if (
                    couponApplyButton &&
                    !couponApplyButton.disabled
                ) {

                    couponForm.requestSubmit();

                }

            }
        );

    }


    /* =========================================================
       PREVENT DOUBLE ORDER SUBMISSION
    ========================================================= */

    if (
        checkoutForm &&
        placeOrderButton
    ) {

        checkoutForm.addEventListener(
            "submit",
            (event) => {

                /*
                 * Ignore submissions that are
                 * not triggered by the main
                 * place-order button.
                 */

                if (
                    event.submitter &&
                    event.submitter !==
                        placeOrderButton
                ) {

                    return;

                }


                /* -----------------------------------------
                   ALREADY SUBMITTING
                ----------------------------------------- */

                if (
                    placeOrderButton.dataset.submitting ===
                    "true"
                ) {

                    event.preventDefault();

                    return;

                }


                /* -----------------------------------------
                   LOCK BUTTON
                ----------------------------------------- */

                placeOrderButton.dataset.submitting =
                    "true";


                placeOrderButton.disabled =
                    true;


                placeOrderButton.dataset.originalText =
                    placeOrderButton.innerHTML;


                placeOrderButton.innerHTML = `
                    <span>PROCESSING...</span>
                `;

            }
        );

    }


    /* =========================================================
       INITIAL COUPON STATE
    ========================================================= */

    if (
        couponApplied &&
        !couponApplied.classList.contains(
            "coupon-hidden"
        )
    ) {

        if (couponForm) {

            couponForm.classList.add(
                "coupon-hidden"
            );

        }

    }


    /* =========================================================
       INITIAL DISCOUNT STATE
    ========================================================= */

    if (
        discountElement &&
        discountRow
    ) {

        const initialDiscount =
            Number(
                discountElement.textContent
            ) || 0;


        if (
            initialDiscount > 0
        ) {

            discountRow.style.display =
                "";

        } else {

            discountRow.style.display =
                "none";

        }

    }

});


/* =========================================================
   NAFI ORDER SUCCESS MODAL
   AUTO REDIRECT TO ORDER DETAILS
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const successModal =
            document.getElementById(
                "nafiOrderSuccessModal"
            );


        /*
         * Modal exists only after
         * successful order creation.
         */

        if (!successModal) {

            return;

        }


        const redirectUrl =
            successModal.dataset.redirectUrl;


        if (!redirectUrl) {

            return;

        }


        /*
         * Keep modal visible long enough
         * for the premium animation.
         */

        const redirectDelay =
            3000;


        setTimeout(
            function () {

                /*
                 * Small fade-out before
                 * redirecting to order details.
                 */

                successModal.style.transition =
                    "opacity 0.35s ease";


                successModal.style.opacity =
                    "0";


                setTimeout(
                    function () {

                        window.location.href =
                            redirectUrl;

                    },
                    350
                );

            },
            redirectDelay
        );

    }
);


/* =========================================================
   NAFI — CITY / DISTRICT → AREA
   DEPENDENT DROPDOWN
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        "use strict";


        /* =====================================================
           ELEMENTS
        ===================================================== */

        const citySelect =
            document.getElementById(
                "city"
            );


        const areaSelect =
            document.getElementById(
                "area"
            );


        const locationDataElement =
            document.getElementById(
                "district-areas-data"
            );


        /* =====================================================
           SAFETY CHECK
        ===================================================== */

        if (
            !citySelect ||
            !areaSelect ||
            !locationDataElement
        ) {

            return;

        }


        /* =====================================================
           LOAD DISTRICT / AREA DATA
        ===================================================== */

        let districtAreas = {};


        try {

            districtAreas =
                JSON.parse(
                    locationDataElement.textContent
                );

        } catch (error) {

            console.error(
                "NAFI: Unable to load district/area data.",
                error
            );


            /*
             * Keep the area field disabled
             * if location data cannot be loaded.
             */

            areaSelect.disabled =
                true;


            return;

        }


        /* =====================================================
           PREVIOUSLY SELECTED AREA
        ===================================================== */

        const previousArea =
            areaSelect.dataset.selectedArea ||
            "";


        /* =====================================================
           POPULATE AREA DROPDOWN
        ===================================================== */

        function populateAreas(
            selectedDistrict,
            selectedArea = ""
        ) {

            /*
             * Always clear old area options.
             */

            areaSelect.innerHTML =
                "";


            /*
             * Default option.
             */

            const defaultOption =
                document.createElement(
                    "option"
                );


            defaultOption.value =
                "";


            defaultOption.textContent =
                "Select Area";


            areaSelect.appendChild(
                defaultOption
            );


            /*
             * No district selected.
             */

            if (
                !selectedDistrict ||
                !districtAreas[
                    selectedDistrict
                ]
            ) {

                areaSelect.disabled =
                    true;


                return;

            }


            /*
             * Enable area dropdown.
             */

            areaSelect.disabled =
                false;


            /*
             * Get areas for selected district.
             */

            const areas =
                districtAreas[
                    selectedDistrict
                ];


            /*
             * Safety check.
             */

            if (
                !Array.isArray(areas)
            ) {

                areaSelect.disabled =
                    true;


                return;

            }


            /*
             * Add area options.
             */

            areas.forEach(
                function (area) {

                    const option =
                        document.createElement(
                            "option"
                        );


                    option.value =
                        area;


                    option.textContent =
                        area;


                    /*
                     * Restore previously
                     * saved area.
                     */

                    if (
                        area ===
                        selectedArea
                    ) {

                        option.selected =
                            true;

                    }


                    areaSelect.appendChild(
                        option
                    );

                }
            );

        }


        /* =====================================================
           DISTRICT CHANGE
        ===================================================== */

        citySelect.addEventListener(
            "change",
            function () {

                /*
                 * When customer manually changes
                 * district, the previous area must
                 * not remain selected.
                 */

                populateAreas(
                    this.value,
                    ""
                );

            }
        );


        /* =====================================================
           INITIAL LOAD
        ===================================================== */

        if (
            citySelect.value
        ) {

            /*
             * Restore saved district + area.
             *
             * This is important for:
             * - Guest customers
             * - Registered customers
             * - Validation errors
             * - Page reloads
             */

            populateAreas(
                citySelect.value,
                previousArea
            );

        } else {

            /*
             * No district selected.
             */

            areaSelect.innerHTML = `
                <option value="">
                    Select Area
                </option>
            `;


            areaSelect.disabled =
                true;

        }

    }
);