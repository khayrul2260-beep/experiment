document.addEventListener("DOMContentLoaded", function () {


    // =====================================================
    // MULTIPLE PRODUCT IMAGE ELEMENTS
    // =====================================================

    const multipleImageUpload =
        document.getElementById("multipleImageUpload");

    const productImagesInput =
        document.getElementById("ProductImages");

    const multipleUploadContent =
        document.getElementById("multipleUploadContent");

    const productImagesPreview =
        document.getElementById("productImagesPreview");

    const productImageCount =
        document.getElementById("productImageCount");


    // =====================================================
    // MULTIPLE IMAGE UPLOAD
    // =====================================================

    if (
        multipleImageUpload &&
        productImagesInput
    ) {

        /*
         * Open file selector
         */

        multipleImageUpload.addEventListener(
            "click",
            function (event) {

                /*
                 * Do not trigger twice when
                 * clicking directly on input.
                 */

                if (
                    event.target !==
                    productImagesInput
                ) {

                    productImagesInput.click();

                }

            }
        );


        /*
         * File selection
         */

        productImagesInput.addEventListener(
            "change",
            function () {

                const files =
                    Array.from(this.files);

                showMultipleImagePreview(files);

            }
        );

    }


    // =====================================================
    // SHOW MULTIPLE IMAGE PREVIEW
    // =====================================================

    function showMultipleImagePreview(files) {

        if (!productImagesPreview) {
            return;
        }


        /*
         * Clear previous preview
         */

        productImagesPreview.innerHTML = "";


        /*
         * No images
         */

        if (!files.length) {

            if (productImageCount) {

                productImageCount.textContent =
                    "No images selected.";

            }

            return;

        }


        /*
         * Image count
         */

        if (productImageCount) {

            productImageCount.textContent =
                `${files.length} image${files.length > 1 ? "s" : ""} selected.`;

        }


        /*
         * Create preview for every image
         */

        files.forEach(
            function (file, index) {


                /*
                 * Validate image
                 */

                if (
                    !file.type.startsWith("image/")
                ) {

                    return;

                }


                const reader =
                    new FileReader();


                reader.onload =
                    function (event) {


                        /*
                         * Preview container
                         */

                        const previewItem =
                            document.createElement(
                                "div"
                            );

                        previewItem.className =
                            "product-image-preview-item";


                        /*
                         * Image
                         */

                        const image =
                            document.createElement(
                                "img"
                            );

                        image.src =
                            event.target.result;

                        image.alt =
                            file.name;


                        /*
                         * Main image badge
                         */

                        if (index === 0) {

                            const badge =
                                document.createElement(
                                    "div"
                                );

                            badge.className =
                                "main-image-badge";

                            badge.textContent =
                                "Main Image";

                            previewItem.appendChild(
                                badge
                            );

                        }


                        /*
                         * Remove button
                         */

                        const removeButton =
                            document.createElement(
                                "button"
                            );

                        removeButton.type =
                            "button";

                        removeButton.className =
                            "remove-product-image";

                        removeButton.innerHTML =
                            '<i class="bi bi-x"></i>';


                        /*
                         * Remove image
                         */

                        removeButton.addEventListener(
                            "click",
                            function (event) {

                                event.preventDefault();

                                event.stopPropagation();

                                removeImage(index);

                            }
                        );


                        /*
                         * Add image
                         */

                        previewItem.appendChild(
                            image
                        );


                        /*
                         * Add remove button
                         */

                        previewItem.appendChild(
                            removeButton
                        );


                        /*
                         * Add preview item
                         */

                        productImagesPreview.appendChild(
                            previewItem
                        );

                    };


                /*
                 * Read image
                 */

                reader.readAsDataURL(file);

            }
        );

    }


    // =====================================================
    // REMOVE IMAGE
    // =====================================================

    function removeImage(index) {

        if (!productImagesInput) {
            return;
        }


        /*
         * Get current files
         */

        const files =
            Array.from(
                productImagesInput.files
            );


        /*
         * Remove selected file
         */

        files.splice(index, 1);


        /*
         * Create new DataTransfer
         */

        const dataTransfer =
            new DataTransfer();


        /*
         * Add remaining files
         */

        files.forEach(
            function (file) {

                dataTransfer.items.add(
                    file
                );

            }
        );


        /*
         * Update input
         */

        productImagesInput.files =
            dataTransfer.files;


        /*
         * Update preview
         */

        showMultipleImagePreview(
            files
        );

    }


    // =====================================================
    // SIZE & STOCK MANAGEMENT
    // =====================================================

    const sizeToggles =
        document.querySelectorAll(
            ".size-toggle"
        );


    const totalStockElement =
        document.getElementById(
            "totalStock"
        );


    // =====================================================
    // UPDATE TOTAL STOCK
    // =====================================================

    function updateTotalStock() {

        let total = 0;


        document
            .querySelectorAll(
                ".size-stock-input"
            )
            .forEach(
                function (input) {

                    if (!input.disabled) {

                        total +=
                            parseInt(
                                input.value
                            ) || 0;

                    }

                }
            );


        if (totalStockElement) {

            totalStockElement.textContent =
                total;

        }

    }


    // =====================================================
    // SIZE CHECKBOX
    // =====================================================

    sizeToggles.forEach(
        function (checkbox) {

            checkbox.addEventListener(
                "change",
                function () {


                    const size =
                        this.dataset.size;


                    const stockInput =
                        document.querySelector(
                            `[data-stock="${size}"]`
                        );


                    if (!stockInput) {
                        return;
                    }


                    /*
                     * Enable stock input
                     */

                    if (this.checked) {

                        stockInput.disabled =
                            false;

                        stockInput.focus();

                    }


                    /*
                     * Disable stock input
                     */

                    else {

                        stockInput.disabled =
                            true;

                        stockInput.value =
                            0;

                    }


                    /*
                     * Update total
                     */

                    updateTotalStock();

                }
            );

        }
    );


    // =====================================================
    // STOCK INPUT CHANGE
    // =====================================================

    document
        .querySelectorAll(
            ".size-stock-input"
        )
        .forEach(
            function (input) {

                input.addEventListener(
                    "input",
                    updateTotalStock
                );

            }
        );


    // =====================================================
    // INITIAL TOTAL STOCK
    // =====================================================

    updateTotalStock();

});

// ==========================================================
// PRODUCT DESCRIPTION EDITOR
// ==========================================================

const descriptionEditorElement =
    document.getElementById("descriptionEditor");

const descriptionInput =
    document.getElementById("description");


if (descriptionEditorElement && descriptionInput) {

    const quill = new Quill(
        "#descriptionEditor",
        {
            theme: "snow",

            placeholder:
                "Write your product description...",

            modules: {

                toolbar: [

                    ["bold", "italic", "underline"],

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

                    ["link"],

                    ["clean"]

                ]

            }

        }
    );


    // ======================================================
    // BEFORE FORM SUBMIT
    // ======================================================

    const productForm =
        descriptionEditorElement.closest("form");


    if (productForm) {

        productForm.addEventListener(
            "submit",
            function () {

                descriptionInput.value =
                    quill.root.innerHTML;

            }
        );

    }

}