document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    /* =========================================================
       ELEMENTS
    ========================================================= */

    const editModal = document.getElementById("editCouponModal");
    const deleteModal = document.getElementById("deleteCouponModal");

    const editForm = document.getElementById("editCouponForm");
    const deleteForm = document.getElementById("deleteCouponForm");

    const editCode = document.getElementById("edit_code");
    const editDescription = document.getElementById("edit_description");
    const editDiscountType = document.getElementById("edit_discount_type");
    const editDiscountValue = document.getElementById("edit_discount_value");
    const editMinimumOrder = document.getElementById("edit_minimum_order_amount");
    const editMaximumDiscount = document.getElementById("edit_maximum_discount");
    const editStartDate = document.getElementById("edit_start_date");
    const editExpiryDate = document.getElementById("edit_expiry_date");
    const editUsageLimit = document.getElementById("edit_usage_limit");
    const editIsActive = document.getElementById("edit_is_active");

    const deleteCouponCode = document.getElementById("delete_coupon_code");


    /* =========================================================
       URL TEMPLATES
       These variables come from coupons.html
    ========================================================= */

    const updateUrlTemplate =
        window.couponUpdateUrlTemplate || "";

    const deleteUrlTemplate =
        window.couponDeleteUrlTemplate || "";


    /* =========================================================
       HELPER
    ========================================================= */

    function buildUrl(template, id) {
        if (!template) {
            return "";
        }

        return template.replace("/0/", `/${id}/`);
    }


    function formatDateTimeLocal(value) {
        if (!value) {
            return "";
        }

        /*
         * Django datetime value may come as:
         * 2026-09-27T15:30:00+06:00
         *
         * datetime-local needs:
         * 2026-09-27T15:30
         */

        return value.substring(0, 16);
    }


    function toggleMaximumDiscount(selectElement, inputElement) {
        if (!selectElement || !inputElement) {
            return;
        }

        if (selectElement.value === "fixed") {
            inputElement.value = "";
            inputElement.disabled = true;
            inputElement.placeholder = "Not applicable";
        } else {
            inputElement.disabled = false;
            inputElement.placeholder = "Optional";
        }
    }


    /* =========================================================
       COUPON CODE — UPPERCASE
    ========================================================= */

    const couponCodeInputs = [
        document.getElementById("code"),
        editCode
    ];

    couponCodeInputs.forEach((input) => {
        if (!input) {
            return;
        }

        input.addEventListener("input", () => {
            input.value = input.value.toUpperCase();
        });
    });


    /* =========================================================
       CREATE MODAL
    ========================================================= */

    const createDiscountType =
        document.getElementById("discount_type");

    const createMaximumDiscount =
        document.getElementById("maximum_discount");

    if (createDiscountType && createMaximumDiscount) {
        toggleMaximumDiscount(
            createDiscountType,
            createMaximumDiscount
        );

        createDiscountType.addEventListener("change", () => {
            toggleMaximumDiscount(
                createDiscountType,
                createMaximumDiscount
            );
        });
    }


    /* =========================================================
       EDIT MODAL
    ========================================================= */

    if (editModal) {
        editModal.addEventListener("show.bs.modal", (event) => {
            const button = event.relatedTarget;

            if (!button) {
                return;
            }

            const couponId = button.dataset.id || "";

            /*
             * Fill form
             */

            if (editCode) {
                editCode.value = button.dataset.code || "";
            }

            if (editDescription) {
                editDescription.value =
                    button.dataset.description || "";
            }

            if (editDiscountType) {
                editDiscountType.value =
                    button.dataset.discountType || "percentage";
            }

            if (editDiscountValue) {
                editDiscountValue.value =
                    button.dataset.discountValue || "";
            }

            if (editMinimumOrder) {
                editMinimumOrder.value =
                    button.dataset.minimumOrder || "0";
            }

            if (editMaximumDiscount) {
                editMaximumDiscount.value =
                    button.dataset.maximumDiscount || "";
            }

            if (editStartDate) {
                editStartDate.value =
                    formatDateTimeLocal(
                        button.dataset.startDate
                    );
            }

            if (editExpiryDate) {
                editExpiryDate.value =
                    formatDateTimeLocal(
                        button.dataset.expiryDate
                    );
            }

            if (editUsageLimit) {
                editUsageLimit.value =
                    button.dataset.usageLimit || "";
            }

            if (editIsActive) {
                editIsActive.checked =
                    button.dataset.isActive === "true";
            }


            /*
             * Set update URL
             */

            if (editForm && updateUrlTemplate) {
                editForm.action =
                    buildUrl(updateUrlTemplate, couponId);
            }


            /*
             * Enable/disable maximum discount
             */

            toggleMaximumDiscount(
                editDiscountType,
                editMaximumDiscount
            );
        });
    }


    /* =========================================================
       EDIT DISCOUNT TYPE CHANGE
    ========================================================= */

    if (editDiscountType && editMaximumDiscount) {
        editDiscountType.addEventListener("change", () => {
            toggleMaximumDiscount(
                editDiscountType,
                editMaximumDiscount
            );
        });
    }


    /* =========================================================
       DELETE MODAL
    ========================================================= */

    if (deleteModal) {
        deleteModal.addEventListener("show.bs.modal", (event) => {
            const button = event.relatedTarget;

            if (!button) {
                return;
            }

            const couponId = button.dataset.id || "";
            const couponCode = button.dataset.code || "";

            if (deleteCouponCode) {
                deleteCouponCode.textContent =
                    couponCode;
            }

            if (deleteForm && deleteUrlTemplate) {
                deleteForm.action =
                    buildUrl(deleteUrlTemplate, couponId);
            }
        });
    }


    /* =========================================================
       NUMBER INPUT PROTECTION
    ========================================================= */

    const decimalInputs = [
        document.getElementById("discount_value"),
        document.getElementById("minimum_order_amount"),
        document.getElementById("maximum_discount"),
        editDiscountValue,
        editMinimumOrder,
        editMaximumDiscount
    ];

    decimalInputs.forEach((input) => {
        if (!input) {
            return;
        }

        input.addEventListener("input", () => {
            if (input.value !== "") {
                const value = parseFloat(input.value);

                if (!Number.isNaN(value) && value < 0) {
                    input.value = "0";
                }
            }
        });
    });


    /* =========================================================
       USAGE LIMIT
    ========================================================= */

    const usageLimitInputs = [
        document.getElementById("usage_limit"),
        editUsageLimit
    ];

    usageLimitInputs.forEach((input) => {
        if (!input) {
            return;
        }

        input.addEventListener("input", () => {
            if (input.value !== "") {
                const value = parseInt(input.value, 10);

                if (!Number.isNaN(value) && value < 0) {
                    input.value = "0";
                }
            }
        });
    });


    /* =========================================================
       FORM VALIDATION
    ========================================================= */

    function validateCouponForm(form) {
        if (!form) {
            return true;
        }

        const discountType =
            form.querySelector('[name="discount_type"]');

        const discountValue =
            form.querySelector('[name="discount_value"]');

        const minimumOrder =
            form.querySelector('[name="minimum_order_amount"]');

        const maximumDiscount =
            form.querySelector('[name="maximum_discount"]');

        const startDate =
            form.querySelector('[name="start_date"]');

        const expiryDate =
            form.querySelector('[name="expiry_date"]');


        /*
         * Discount value
         */

        if (
            discountValue &&
            parseFloat(discountValue.value || "0") <= 0
        ) {
            alert("Discount value must be greater than 0.");
            discountValue.focus();
            return false;
        }


        /*
         * Minimum order
         */

        if (
            minimumOrder &&
            parseFloat(minimumOrder.value || "0") < 0
        ) {
            alert("Minimum order amount cannot be negative.");
            minimumOrder.focus();
            return false;
        }


        /*
         * Percentage
         */

        if (
            discountType &&
            discountType.value === "percentage" &&
            parseFloat(discountValue?.value || "0") > 100
        ) {
            alert("Percentage discount cannot exceed 100%.");
            discountValue.focus();
            return false;
        }


        /*
         * Maximum discount
         */

        if (
            discountType &&
            discountType.value === "percentage" &&
            maximumDiscount &&
            maximumDiscount.value !== "" &&
            parseFloat(maximumDiscount.value) < 0
        ) {
            alert("Maximum discount cannot be negative.");
            maximumDiscount.focus();
            return false;
        }


        /*
         * Date validation
         */

        if (
            startDate &&
            expiryDate &&
            startDate.value &&
            expiryDate.value
        ) {
            const start = new Date(startDate.value);
            const expiry = new Date(expiryDate.value);

            if (expiry <= start) {
                alert(
                    "Expiry date must be later than the start date."
                );

                expiryDate.focus();
                return false;
            }
        }

        return true;
    }


    /* =========================================================
       CREATE FORM
    ========================================================= */

    const createForm =
        document.getElementById("createCouponForm");

    if (createForm) {
        createForm.addEventListener("submit", (event) => {
            if (!validateCouponForm(createForm)) {
                event.preventDefault();
            }
        });
    }


    /* =========================================================
       EDIT FORM
    ========================================================= */

    if (editForm) {
        editForm.addEventListener("submit", (event) => {
            if (!validateCouponForm(editForm)) {
                event.preventDefault();
            }
        });
    }


    /* =========================================================
       AUTO DEFAULT DATE
    ========================================================= */

    function getLocalDateTime() {
        const now = new Date();

        const year = now.getFullYear();
        const month = String(
            now.getMonth() + 1
        ).padStart(2, "0");

        const day = String(
            now.getDate()
        ).padStart(2, "0");

        const hours = String(
            now.getHours()
        ).padStart(2, "0");

        const minutes = String(
            now.getMinutes()
        ).padStart(2, "0");

        return `${year}-${month}-${day}T${hours}:${minutes}`;
    }


    const createStartDate =
        document.getElementById("start_date");

    const createExpiryDate =
        document.getElementById("expiry_date");

    if (createStartDate && !createStartDate.value) {
        createStartDate.value =
            getLocalDateTime();
    }


    if (createExpiryDate && !createExpiryDate.value) {
        const expiry = new Date();
        expiry.setDate(
            expiry.getDate() + 7
        );

        const year = expiry.getFullYear();

        const month = String(
            expiry.getMonth() + 1
        ).padStart(2, "0");

        const day = String(
            expiry.getDate()
        ).padStart(2, "0");

        const hours = String(
            expiry.getHours()
        ).padStart(2, "0");

        const minutes = String(
            expiry.getMinutes()
        ).padStart(2, "0");

        createExpiryDate.value =
            `${year}-${month}-${day}T${hours}:${minutes}`;
    }


    /* =========================================================
       RESET CREATE MODAL
    ========================================================= */

    const createModal =
        document.getElementById("createCouponModal");

    if (createModal) {
        createModal.addEventListener(
            "hidden.bs.modal",
            () => {
                if (createForm) {
                    createForm.reset();
                }

                if (
                    createDiscountType &&
                    createMaximumDiscount
                ) {
                    createDiscountType.value =
                        "percentage";

                    createMaximumDiscount.disabled =
                        false;

                    createMaximumDiscount.placeholder =
                        "Optional";
                }
            }
        );
    }


    /* =========================================================
       CONSOLE CHECK
    ========================================================= */

    console.log(
        "NAFI Coupon Management JS loaded successfully."
    );
});