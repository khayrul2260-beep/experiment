document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // NAFI — PRODUCT DESCRIPTION / QUILL EDITOR
    // =====================================================


    // =====================================================
    // ELEMENTS
    // =====================================================

    const descriptionEditor =
        document.getElementById("productDescription");

    const descriptionInput =
        document.getElementById("description");

    const productForm =
        document.getElementById("productForm");


    // =====================================================
    // CHECK REQUIRED ELEMENTS
    // =====================================================

    if (!descriptionEditor) {

        console.error(
            "Quill editor element #productDescription was not found."
        );

        return;
    }


    if (!descriptionInput) {

        console.error(
            "Description textarea #description was not found."
        );

        return;
    }


    if (!productForm) {

        console.error(
            "Product form #productForm was not found."
        );

        return;
    }


    // =====================================================
    // CHECK QUILL
    // =====================================================

    if (typeof Quill === "undefined") {

        console.error(
            "Quill is not loaded. Make sure quill.js is loaded before product_description.js."
        );

        return;
    }


    // =====================================================
    // INITIALIZE QUILL
    // =====================================================

    const quill = new Quill(
        descriptionEditor,
        {

            theme: "snow",

            placeholder:
                "Write product description...",

            modules: {

                toolbar: [

                    [
                        "bold",
                        "italic",
                        "underline",
                        "strike"
                    ],

                    [
                        {
                            header: [1, 2, 3, false]
                        }
                    ],

                    [
                        {
                            list: "ordered"
                        },
                        {
                            list: "bullet"
                        }
                    ],

                    [
                        {
                            align: []
                        }
                    ],

                    [
                        "blockquote",
                        "link"
                    ],

                    [
                        "clean"
                    ]

                ]

            }

        }
    );


    // =====================================================
    // LOAD EXISTING DESCRIPTION
    // Edit Product Page
    // =====================================================

    const existingDescription =
        descriptionInput.value.trim();


    if (existingDescription !== "") {

        quill.root.innerHTML =
            existingDescription;

    }


    // =====================================================
    // SYNC QUILL → TEXTAREA
    // =====================================================

    function syncDescription() {

        descriptionInput.value =
            quill.root.innerHTML;

    }


    // =====================================================
    // QUILL CONTENT CHANGE
    // =====================================================

    quill.on(
        "text-change",
        function () {

            syncDescription();

        }
    );


    // =====================================================
    // INITIAL SYNC
    // =====================================================

    syncDescription();


    // =====================================================
    // FORM SUBMIT
    // =====================================================

    productForm.addEventListener(
        "submit",
        function (event) {

            // -------------------------------------------------
            // Always sync immediately before submission
            // -------------------------------------------------

            syncDescription();


            // -------------------------------------------------
            // Get plain text from Quill
            // -------------------------------------------------

            const descriptionText =
                quill
                    .getText()
                    .trim();


            // -------------------------------------------------
            // Validate empty description
            // -------------------------------------------------

            if (!descriptionText) {

                event.preventDefault();


                alert(
                    "Please enter a product description."
                );


                quill.focus();

                return;
            }


            // -------------------------------------------------
            // Final sync
            // -------------------------------------------------

            syncDescription();

        }
    );


    // =====================================================
    // DEBUG
    // =====================================================

    console.log(
        "NAFI Product Description — Quill initialized successfully."
    );

});

