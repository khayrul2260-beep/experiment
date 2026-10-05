document.addEventListener("DOMContentLoaded", () => {
    "use strict";


    /* =========================================================
       ELEMENTS
    ========================================================= */

    const couponForm = document.getElementById("coupon-form");
    const couponInput = document.getElementById("coupon-code");
    const couponApplyButton = document.getElementById("coupon-apply-btn");

    const couponApplied = document.getElementById("coupon-applied");
    const couponAppliedCode = document.getElementById("coupon-applied-code");
    const couponRemoveButton = document.getElementById("coupon-remove-btn");
    const couponMessage = document.getElementById("coupon-message");

    const subtotalElement = document.getElementById("checkout-subtotal");
    const discountElement = document.getElementById("checkout-discount");
    const discountRow = document.getElementById("checkout-discount-row");
    const deliveryElement = document.getElementById("checkout-delivery");
    const totalElement = document.getElementById("checkout-total");

    const checkoutForm = document.getElementById("checkout-form");
    const placeOrderButton = document.getElementById("place-order-btn");


    /* =========================================================
       STOP IF CHECKOUT ELEMENTS ARE NOT AVAILABLE
    ========================================================= */

    if (!couponForm) {
        return;
    }


    /* =========================================================
       CSRF TOKEN
    ========================================================= */

    function getCSRFToken() {

        const csrfInput = document.querySelector(
            'input[name="csrfmiddlewaretoken"]'
        );

        if (csrfInput && csrfInput.value) {
            return csrfInput.value;
        }


        const cookie = document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="));


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

        const number = Number(value || 0);

        return number.toFixed(2);
    }


    /* =========================================================
       COUPON MESSAGE
    ========================================================= */

    function showCouponMessage(message, type = "error") {

        if (!couponMessage) {
            return;
        }


        couponMessage.textContent = message || "";


        couponMessage.classList.remove(
            "show",
            "success",
            "error"
        );


        if (type === "success") {

            couponMessage.classList.add("success");

        } else {

            couponMessage.classList.add("error");

        }


        couponMessage.classList.add("show");
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
                formatMoney(data.subtotal);

        }


        if (
            discountElement &&
            data.discount !== undefined
        ) {

            const discount =
                Number(data.discount || 0);


            discountElement.textContent =
                formatMoney(discount);


            /*
             * Show/hide discount row automatically.
             */

            if (discountRow) {

                if (discount > 0) {

                    discountRow.style.display = "";

                } else {

                    discountRow.style.display = "none";

                }

            }

        }


        if (
            deliveryElement &&
            data.delivery_charge !== undefined
        ) {

            deliveryElement.textContent =
                formatMoney(data.delivery_charge);

        }


        if (
            totalElement &&
            data.total_amount !== undefined
        ) {

            totalElement.textContent =
                formatMoney(data.total_amount);

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

    function setApplyLoading(isLoading) {

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


            couponApplyButton.disabled = true;

            couponApplyButton.textContent =
                "APPLYING...";

        } else {

            couponApplyButton.disabled = false;

            couponApplyButton.textContent =
                couponApplyButton.dataset.originalText ||
                "APPLY";

        }

    }


    /* =========================================================
       REMOVE BUTTON LOADING
    ========================================================= */

    function setRemoveLoading(isLoading) {

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


            couponRemoveButton.disabled = true;

            couponRemoveButton.textContent =
                "REMOVING...";

        } else {

            couponRemoveButton.disabled = false;

            couponRemoveButton.textContent =
                couponRemoveButton.dataset.originalText ||
                "REMOVE";

        }

    }


    /* =========================================================
       SERVER REQUEST
    ========================================================= */

    async function sendPostRequest(url, data = {}) {

        const response = await fetch(
            url,
            {
                method: "POST",

                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type":
                        "application/x-www-form-urlencoded; charset=UTF-8"
                },

                body: new URLSearchParams(data)
            }
        );


        let result;


        try {

            result = await response.json();

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

    couponForm.addEventListener(
        "submit",
        async (event) => {

            event.preventDefault();


            const code = couponInput
                ? couponInput.value.trim()
                : "";


            hideCouponMessage();


            /* ---------------------------------------------
               EMPTY CODE
            --------------------------------------------- */

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
                } = await sendPostRequest(
                    couponForm.action,
                    {
                        code: code
                    }
                );


                /* -----------------------------------------
                   INVALID COUPON
                ----------------------------------------- */

                if (
                    !response.ok ||
                    !data.success
                ) {

                    if (
                        data.subtotal !== undefined
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


                /* -----------------------------------------
                   VALID COUPON
                ----------------------------------------- */

                updateSummary(data);


                showAppliedCoupon(
                    data.coupon_code || code
                );


                showCouponMessage(
                    data.message ||
                    "Coupon applied successfully.",
                    "success"
                );


                if (couponInput) {

                    couponInput.value = "";

                }

            } catch (error) {

                console.error(
                    "Apply coupon error:",
                    error
                );


                showCouponMessage(
                    "Something went wrong. Please try again.",
                    "error"
                );

            } finally {

                setApplyLoading(false);

            }

        }
    );


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
                    } = await sendPostRequest(
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


                    updateSummary(data);

                    showCouponForm();


                    if (couponInput) {

                        couponInput.value = "";

                    }


                    showCouponMessage(
                        data.message ||
                        "Coupon removed successfully.",
                        "success"
                    );

                } catch (error) {

                    console.error(
                        "Remove coupon error:",
                        error
                    );


                    showCouponMessage(
                        "Something went wrong. Please try again.",
                        "error"
                    );

                } finally {

                    setRemoveLoading(false);

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
       ENTER KEY
    ========================================================= */

    if (couponInput) {

        couponInput.addEventListener(
            "keydown",
            (event) => {

                if (event.key !== "Enter") {
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

    if (checkoutForm && placeOrderButton) {

        checkoutForm.addEventListener(
            "submit",
            (event) => {

                /*
                 * Coupon form has its own submit handler,
                 * so this only handles the main checkout
                 * form submission.
                 */

                if (
                    event.submitter &&
                    event.submitter !== placeOrderButton
                ) {

                    return;

                }


                if (
                    placeOrderButton.dataset.submitting ===
                    "true"
                ) {

                    event.preventDefault();

                    return;

                }


                placeOrderButton.dataset.submitting =
                    "true";


                placeOrderButton.disabled = true;


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


        if (initialDiscount > 0) {

            discountRow.style.display = "";

        } else {

            discountRow.style.display = "none";

        }

    }

});


/* =========================================================
   NAFI ORDER SUCCESS MODAL
   Auto redirect to Order Details
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const successModal = document.getElementById("nafiOrderSuccessModal");

    // Modal exists only after successful order creation
    if (!successModal) {
        return;
    }

    const redirectUrl = successModal.dataset.redirectUrl;

    if (!redirectUrl) {
        return;
    }

    /*
     * Keep the modal visible long enough
     * for the premium animation to complete.
     */
    const redirectDelay = 3000;

    setTimeout(function () {

        /*
         * Small fade-out before leaving checkout.
         * The modal itself remains visible during
         * almost the entire 3-second experience.
         */
        successModal.style.transition =
            "opacity 0.35s ease";

        successModal.style.opacity = "0";

        setTimeout(function () {
            window.location.href = redirectUrl;
        }, 350);

    }, redirectDelay);

});


// =========================================================
// NAFI — CITY / DISTRICT → AREA DEPENDENT DROPDOWN
// =========================================================

document.addEventListener("DOMContentLoaded", function () {

    const citySelect = document.getElementById("city");
    const areaSelect = document.getElementById("area");
    const locationDataElement =
        document.getElementById("district-areas-data");


    // -----------------------------------------------------
    // SAFETY CHECK
    // -----------------------------------------------------

    if (
        !citySelect ||
        !areaSelect ||
        !locationDataElement
    ) {
        return;
    }


    // -----------------------------------------------------
    // LOCATION DATA
    // -----------------------------------------------------

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

        return;
    }


    // -----------------------------------------------------
    // PREVIOUSLY SELECTED AREA
    // -----------------------------------------------------

    const previousArea =
        areaSelect.dataset.selectedArea || "";


    // -----------------------------------------------------
    // POPULATE AREA DROPDOWN
    // -----------------------------------------------------

    function populateAreas(
        selectedDistrict,
        selectedArea = ""
    ) {

        // Clear existing options

        areaSelect.innerHTML = "";


        // Default option

        const defaultOption =
            document.createElement("option");

        defaultOption.value = "";
        defaultOption.textContent =
            "Select Area";

        areaSelect.appendChild(defaultOption);


        // No district selected

        if (
            !selectedDistrict ||
            !districtAreas[selectedDistrict]
        ) {

            areaSelect.disabled = true;

            return;
        }


        // Enable area dropdown

        areaSelect.disabled = false;


        // Add areas

        districtAreas[selectedDistrict].forEach(
            function (area) {

                const option =
                    document.createElement("option");

                option.value = area;
                option.textContent = area;


                // Restore previous selection

                if (area === selectedArea) {
                    option.selected = true;
                }


                areaSelect.appendChild(option);

            }
        );

    }


    // -----------------------------------------------------
    // DISTRICT CHANGE
    // -----------------------------------------------------

    citySelect.addEventListener(
        "change",
        function () {

            populateAreas(
                this.value
            );

        }
    );


    // -----------------------------------------------------
    // INITIAL LOAD
    // -----------------------------------------------------

    if (citySelect.value) {

        populateAreas(
            citySelect.value,
            previousArea
        );

    } else {

        areaSelect.disabled = true;

    }

});

