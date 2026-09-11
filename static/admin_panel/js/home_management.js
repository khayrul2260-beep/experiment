document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       ELEMENTS
    ===================================================== */

    const desktopInput = document.getElementById("desktop_image");
    const mobileInput = document.getElementById("mobile_image");

    const desktopMessage =
        document.getElementById("desktopValidation");

    const mobileMessage =
        document.getElementById("mobileValidation");

    const heroForm =
        document.getElementById("heroSlideForm");


    /* =====================================================
       VALIDATE IMAGE
    ===================================================== */

    function validateImage(
        input,
        messageElement,
        requiredWidth,
        requiredHeight,
        imageName
    ) {

        return new Promise(function (resolve) {

            const file = input.files[0];

            if (!file) {

                messageElement.className =
                    "image-validation-message";

                messageElement.textContent = "";

                resolve(false);

                return;
            }


            /* =============================================
               FILE TYPE
            ============================================= */

            const allowedTypes = [
                "image/jpeg",
                "image/png",
                "image/webp"
            ];


            if (!allowedTypes.includes(file.type)) {

                messageElement.className =
                    "image-validation-message invalid";

                messageElement.textContent =
                    "✕ Invalid file type. Please upload JPG, PNG or WEBP.";

                input.value = "";

                resolve(false);

                return;
            }


            /* =============================================
               IMAGE DIMENSION
            ============================================= */

            const image = new Image();

            const objectUrl =
                URL.createObjectURL(file);


            image.onload = function () {

                const width = image.naturalWidth;
                const height = image.naturalHeight;

                URL.revokeObjectURL(objectUrl);


                if (
                    width === requiredWidth &&
                    height === requiredHeight
                ) {

                    messageElement.className =
                        "image-validation-message valid";

                    messageElement.textContent =
                        "✓ Valid image — " +
                        width +
                        " × " +
                        height +
                        " px";

                    resolve(true);

                    return;
                }


                messageElement.className =
                    "image-validation-message invalid";

                messageElement.textContent =
                    "✕ Invalid size: " +
                    width +
                    " × " +
                    height +
                    " px. " +
                    imageName +
                    " must be exactly " +
                    requiredWidth +
                    " × " +
                    requiredHeight +
                    " px.";

                input.value = "";

                resolve(false);

            };


            image.onerror = function () {

                URL.revokeObjectURL(objectUrl);

                messageElement.className =
                    "image-validation-message invalid";

                messageElement.textContent =
                    "✕ Unable to read this image.";

                input.value = "";

                resolve(false);

            };


            image.src = objectUrl;

        });

    }


    /* =====================================================
       DESKTOP
    ===================================================== */

    if (desktopInput) {

        desktopInput.addEventListener(
            "change",
            function () {

                validateImage(
                    desktopInput,
                    desktopMessage,
                    1968,
                    799,
                    "Desktop image"
                );

            }
        );

    }


    /* =====================================================
       MOBILE
    ===================================================== */

    if (mobileInput) {

        mobileInput.addEventListener(
            "change",
            function () {

                validateImage(
                    mobileInput,
                    mobileMessage,
                    900,
                    1600,
                    "Mobile image"
                );

            }
        );

    }


    /* =====================================================
       FORM SUBMIT
    ===================================================== */

    if (heroForm) {

        heroForm.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();


                const desktopValid =
                    await validateImage(
                        desktopInput,
                        desktopMessage,
                        1968,
                        799,
                        "Desktop image"
                    );


                const mobileValid =
                    await validateImage(
                        mobileInput,
                        mobileMessage,
                        900,
                        1600,
                        "Mobile image"
                    );


                if (!desktopValid || !mobileValid) {
                    return;
                }


                heroForm.submit();

            }
        );

    }

    const secondHeroInput =
        document.getElementById("secondHeroImage");

    if (secondHeroInput) {

        secondHeroInput.addEventListener("change", function () {

            const file = this.files[0];
            const message =
                document.getElementById("secondHeroImageMessage");

            if (!file) return;

            const img = new Image();

            img.onload = function () {

                if (this.width !== 1968 || this.height !== 799) {

                    message.textContent =
                        "Invalid image. Required size: 1968 × 799 px.";

                    message.style.color = "var(--danger)";

                    secondHeroInput.value = "";

                } else {

                    message.textContent =
                        "✓ Image size is valid (1968 × 799 px).";

                    message.style.color = "var(--success)";
                }

                URL.revokeObjectURL(img.src);
            };

            img.src = URL.createObjectURL(file);
        });
    }
    
});

document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll('[id^="editSlideModal"]').forEach(function (modal) {

        modal.addEventListener("shown.bs.modal", function () {
            document.body.classList.add("nafi-modal-page-scroll");
        });

        modal.addEventListener("hidden.bs.modal", function () {
            document.body.classList.remove("nafi-modal-page-scroll");
        });

    });

});

