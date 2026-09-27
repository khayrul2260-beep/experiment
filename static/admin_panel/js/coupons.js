(function () {
    "use strict";


    /* =====================================================
       ELEMENT HELPERS
    ===================================================== */

    function getElement(id) {
        return document.getElementById(id);
    }


    function getElements(selector) {
        return document.querySelectorAll(selector);
    }


    function setValue(id, value) {
        const element = getElement(id);

        if (element) {
            element.value = value ?? "";
        }
    }


    function setChecked(id, value) {
        const element = getElement(id);

        if (element) {
            element.checked = Boolean(value);
        }
    }


    /* =====================================================
       MODAL HELPERS
    ===================================================== */

    function openModal(modal) {

        if (!modal) {
            return;
        }

        modal.classList.add("is-open");
        modal.setAttribute("aria-hidden", "false");

        document.body.classList.add("coupon-modal-open");
    }


    function closeModal(modal) {

        if (!modal) {
            return;
        }

        modal.classList.remove("is-open");
        modal.setAttribute("aria-hidden", "true");

        if (!document.querySelector(".coupon-modal.is-open")) {
            document.body.classList.remove("coupon-modal-open");
        }
    }


    function closeAllModals() {

        getElements(".coupon-modal.is-open").forEach(function (modal) {
            modal.classList.remove("is-open");
            modal.setAttribute("aria-hidden", "true");
        });

        document.body.classList.remove("coupon-modal-open");
    }


    /* =====================================================
       MODALS
    ===================================================== */

    const createModal = getElement("createCouponModal");
    const editModal = getElement("editCouponModal");
    const deleteModal = getElement("deleteCouponModal");


    /* =====================================================
       OPEN CREATE MODAL
    ===================================================== */

    const createButtons = [
        getElement("openCreateCoupon"),
        getElement("openCreateCouponEmpty")
    ];


    createButtons.forEach(function (button) {

        if (!button) {
            return;
        }

        button.addEventListener("click", function () {

            resetCreateForm();

            openModal(createModal);

            const codeInput = getElement("createCouponCode");

            if (codeInput) {
                setTimeout(function () {
                    codeInput.focus();
                }, 150);
            }

        });

    });


    /* =====================================================
       CLOSE MODALS
    ===================================================== */

    getElements("[data-close-modal]").forEach(function (button) {

        button.addEventListener("click", function () {

            const modal = button.closest(".coupon-modal");

            closeModal(modal);

        });

    });


    /* =====================================================
       CLOSE BY OVERLAY
    ===================================================== */

    getElements(".coupon-modal-overlay").forEach(function (overlay) {

        overlay.addEventListener("click", function () {

            const modal = overlay.closest(".coupon-modal");

            closeModal(modal);

        });

    });


    /* =====================================================
       ESCAPE KEY
    ===================================================== */

    document.addEventListener("keydown", function (event) {

        if (event.key !== "Escape") {
            return;
        }

        closeAllModals();

    });


    /* =====================================================
       BODY SCROLL CONTROL
    ===================================================== */

    const style = document.createElement("style");

    style.textContent = `
        body.coupon-modal-open {
            overflow: hidden;
        }
    `;

    document.head.appendChild(style);


    /* =====================================================
       DATE HELPERS
    ===================================================== */

    function formatDateTimeLocal(dateValue) {

        if (!dateValue) {
            return "";
        }

        const date = new Date(dateValue);

        if (Number.isNaN(date.getTime())) {
            return "";
        }

        const year = date.getFullYear();

        const month = String(
            date.getMonth() + 1
        ).padStart(2, "0");

        const day = String(
            date.getDate()
        ).padStart(2, "0");

        const hours = String(
            date.getHours()
        ).padStart(2, "0");

        const minutes = String(
            date.getMinutes()
        ).padStart(2, "0");

        return `${year}-${month}-${day}T${hours}:${minutes}`;
    }


    function getLocalDateTimePlusDays(days) {

        const date = new Date();

        date.setDate(
            date.getDate() + days
        );

        return formatDateTimeLocal(date);
    }


    /* =====================================================
       CREATE FORM RESET
    ===================================================== */

    function resetCreateForm() {

        const form = getElement("createCouponForm");

        if (!form) {
            return;
        }

        form.reset();

        setValue(
            "createStartDate",
            formatDateTimeLocal(new Date())
        );

        setValue(
            "createExpiryDate",
            getLocalDateTimePlusDays(7)
        );

        setValue(
            "createMinimumOrder",
            "0"
        );

        setChecked(
            "createIsActive",
            true
        );

        updateCreateDiscountFields();

    }


    /* =====================================================
       EDIT FORM RESET
    ===================================================== */

    function resetEditForm() {

        const form = getElement("editCouponForm");

        if (!form) {
            return;
        }

        form.reset();

    }


    /* =====================================================
       UPPERCASE COUPON CODE
    ===================================================== */

    function normalizeCouponCode(input) {

        if (!input) {
            return;
        }

        input.addEventListener("input", function () {

            input.value = input.value
                .toUpperCase()
                .replace(/\s+/g, "");

        });

    }


    normalizeCouponCode(
        getElement("createCouponCode")
    );


    normalizeCouponCode(
        getElement("editCouponCode")
    );


    /* =====================================================
       DISCOUNT TYPE
    ===================================================== */

    const createDiscountType =
        getElement("createDiscountType");

    const editDiscountType =
        getElement("editDiscountType");


    function updateDiscountFields(
        typeElement,
        maximumInput
    ) {

        if (!typeElement || !maximumInput) {
            return;
        }

        if (typeElement.value === "percentage") {

            maximumInput.placeholder =
                "Optional";

        } else {

            maximumInput.placeholder =
                "Optional maximum amount";

        }

    }


    function updateCreateDiscountFields() {

        updateDiscountFields(
            createDiscountType,
            getElement("createMaximumDiscount")
        );

    }


    function updateEditDiscountFields() {

        updateDiscountFields(
            editDiscountType,
            getElement("editMaximumDiscount")
        );

    }


    if (createDiscountType) {

        createDiscountType.addEventListener(
            "change",
            updateCreateDiscountFields
        );

    }


    if (editDiscountType) {

        editDiscountType.addEventListener(
            "change",
            updateEditDiscountFields
        );

    }


    /* =====================================================
       URL BUILDER
    ===================================================== */

    function buildUrl(template, id) {

        if (!template || !id) {
            return "";
        }

        return template.replace(
            "/0/",
            `/${id}/`
        );

    }


    /* =====================================================
       EDIT COUPON
    ===================================================== */

    getElements(".coupon-edit-btn").forEach(function (button) {

        button.addEventListener("click", function () {

            const id = button.dataset.id;

            if (!id) {
                return;
            }


            resetEditForm();


            /* ---------------------------------------------
               Fill form
            --------------------------------------------- */

            setValue(
                "editCouponCode",
                button.dataset.code
            );


            setValue(
                "editCouponDescription",
                button.dataset.description
            );


            setValue(
                "editDiscountType",
                button.dataset.discountType
            );


            setValue(
                "editDiscountValue",
                button.dataset.discountValue
            );


            setValue(
                "editMinimumOrder",
                button.dataset.minimumOrder
            );


            setValue(
                "editMaximumDiscount",
                button.dataset.maximumDiscount
            );


            setValue(
                "editStartDate",
                formatDateTimeLocal(
                    button.dataset.startDate
                )
            );


            setValue(
                "editExpiryDate",
                formatDateTimeLocal(
                    button.dataset.expiryDate
                )
            );


            setValue(
                "editUsageLimit",
                button.dataset.usageLimit
            );


            setChecked(
                "editIsActive",
                button.dataset.isActive === "true"
            );


            updateEditDiscountFields();


            /* ---------------------------------------------
               Dynamic form action
            --------------------------------------------- */

            const editForm =
                getElement("editCouponForm");

            if (editForm) {

                editForm.action = buildUrl(
                    window.couponUpdateUrlTemplate,
                    id
                );

            }


            /* ---------------------------------------------
               Open modal
            --------------------------------------------- */

            openModal(editModal);


            const codeInput =
                getElement("editCouponCode");

            if (codeInput) {

                setTimeout(function () {
                    codeInput.focus();
                }, 150);

            }

        });

    });


    /* =====================================================
       DELETE COUPON
    ===================================================== */

    getElements(".coupon-delete-btn").forEach(function (button) {

        button.addEventListener("click", function () {

            const id = button.dataset.id;
            const code = button.dataset.code;

            if (!id) {
                return;
            }


            const codeElement =
                getElement("deleteCouponCode");

            if (codeElement) {

                codeElement.textContent =
                    code || "this coupon";

            }


            const deleteForm =
                getElement("deleteCouponForm");

            if (deleteForm) {

                deleteForm.action = buildUrl(
                    window.couponDeleteUrlTemplate,
                    id
                );

            }


            openModal(deleteModal);

        });

    });


    /* =====================================================
       CREATE VALIDATION
    ===================================================== */

    const createForm =
        getElement("createCouponForm");


    if (createForm) {

        createForm.addEventListener(
            "submit",
            function (event) {

                const code =
                    getElement("createCouponCode");

                const discountType =
                    getElement("createDiscountType");

                const discountValue =
                    getElement("createDiscountValue");

                const minimumOrder =
                    getElement("createMinimumOrder");

                const maximumDiscount =
                    getElement("createMaximumDiscount");

                const startDate =
                    getElement("createStartDate");

                const expiryDate =
                    getElement("createExpiryDate");


                /* -----------------------------------------
                   Code
                ----------------------------------------- */

                if (
                    !code ||
                    !code.value.trim()
                ) {

                    event.preventDefault();

                    if (code) {
                        code.focus();
                    }

                    return;

                }


                /* -----------------------------------------
                   Discount
                ----------------------------------------- */

                const discount =
                    Number(discountValue.value);


                if (
                    !discountValue.value ||
                    Number.isNaN(discount) ||
                    discount <= 0
                ) {

                    event.preventDefault();

                    discountValue.focus();

                    return;

                }


                if (
                    discountType.value === "percentage" &&
                    discount > 100
                ) {

                    event.preventDefault();

                    discountValue.focus();

                    return;

                }


                /* -----------------------------------------
                   Minimum order
                ----------------------------------------- */

                const minimum =
                    Number(minimumOrder.value || 0);


                if (
                    Number.isNaN(minimum) ||
                    minimum < 0
                ) {

                    event.preventDefault();

                    minimumOrder.focus();

                    return;

                }


                /* -----------------------------------------
                   Maximum discount
                ----------------------------------------- */

                if (maximumDiscount.value) {

                    const maximum =
                        Number(maximumDiscount.value);

                    if (
                        Number.isNaN(maximum) ||
                        maximum < 0
                    ) {

                        event.preventDefault();

                        maximumDiscount.focus();

                        return;

                    }

                }


                /* -----------------------------------------
                   Dates
                ----------------------------------------- */

                if (
                    startDate.value &&
                    expiryDate.value
                ) {

                    const start =
                        new Date(startDate.value);

                    const expiry =
                        new Date(expiryDate.value);


                    if (expiry <= start) {

                        event.preventDefault();

                        expiryDate.focus();

                        return;

                    }

                }

            }
        );

    }


    /* =====================================================
       EDIT VALIDATION
    ===================================================== */

    const editForm =
        getElement("editCouponForm");


    if (editForm) {

        editForm.addEventListener(
            "submit",
            function (event) {

                const discountType =
                    getElement("editDiscountType");

                const discountValue =
                    getElement("editDiscountValue");

                const startDate =
                    getElement("editStartDate");

                const expiryDate =
                    getElement("editExpiryDate");


                const discount =
                    Number(discountValue.value);


                if (
                    !discountValue.value ||
                    Number.isNaN(discount) ||
                    discount <= 0
                ) {

                    event.preventDefault();

                    discountValue.focus();

                    return;

                }


                if (
                    discountType.value === "percentage" &&
                    discount > 100
                ) {

                    event.preventDefault();

                    discountValue.focus();

                    return;

                }


                if (
                    startDate.value &&
                    expiryDate.value
                ) {

                    const start =
                        new Date(startDate.value);

                    const expiry =
                        new Date(expiryDate.value);


                    if (expiry <= start) {

                        event.preventDefault();

                        expiryDate.focus();

                        return;

                    }

                }

            }
        );

    }


    /* =====================================================
       PREVENT DOUBLE SUBMIT
    ===================================================== */

    getElements(
        "#createCouponForm, #editCouponForm, #deleteCouponForm"
    ).forEach(function (form) {

        form.addEventListener(
            "submit",
            function () {

                const submitButton =
                    form.querySelector(
                        'button[type="submit"]'
                    );


                if (!submitButton) {
                    return;
                }


                submitButton.disabled = true;

                submitButton.style.opacity = "0.55";

                submitButton.style.cursor =
                    "not-allowed";

            }
        );

    });


    /* =====================================================
       INITIALIZE
    ===================================================== */

    updateCreateDiscountFields();
    updateEditDiscountFields();

})();