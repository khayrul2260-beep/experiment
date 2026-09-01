document.addEventListener("DOMContentLoaded", function () {


    // =====================================================
    // PRODUCT IMAGE MANAGEMENT
    // Main + Secondary + Gallery
    // =====================================================


    // =====================================================
    // MAIN IMAGE ELEMENTS
    // =====================================================

    const mainImageUpload =
        document.getElementById("mainImageUpload");

    const mainImageInput =
        document.getElementById("mainImageInput");

    const mainUploadContent =
        document.getElementById("mainUploadContent");

    const mainImagePreview =
        document.getElementById("mainImagePreview");


    // =====================================================
    // SECONDARY IMAGE ELEMENTS
    // =====================================================

    const secondaryImageUpload =
        document.getElementById("secondaryImageUpload");

    const secondaryImageInput =
        document.getElementById("secondaryImageInput");

    const secondaryUploadContent =
        document.getElementById("secondaryUploadContent");

    const secondaryImagePreview =
        document.getElementById("secondaryImagePreview");


    // =====================================================
    // GALLERY IMAGE ELEMENTS
    // =====================================================

    const galleryImageUpload =
        document.getElementById("galleryImageUpload");

    const galleryImagesInput =
        document.getElementById("galleryImagesInput");

    const galleryUploadContent =
        document.getElementById("galleryUploadContent");

    const galleryImagesPreview =
        document.getElementById("galleryImagesPreview");

    const galleryImageCount =
        document.getElementById("galleryImageCount");


    // =====================================================
    // SINGLE IMAGE PREVIEW
    // =====================================================

    function showSingleImagePreview(
        input,
        previewContainer,
        uploadContainer,
        uploadContent
    ) {

        if (
            !input ||
            !previewContainer
        ) {
            return;
        }


        const file =
            input.files[0];


        // -------------------------------------------------
        // No image selected
        // -------------------------------------------------

        if (!file) {

            previewContainer.innerHTML = "";

            previewContainer.classList.remove(
                "active"
            );

            if (uploadContainer) {

                uploadContainer.classList.remove(
                    "has-image"
                );

            }

            if (uploadContent) {

                uploadContent.style.display =
                    "flex";

            }

            return;
        }


        // -------------------------------------------------
        // Validate image
        // -------------------------------------------------

        if (
            !file.type.startsWith("image/")
        ) {

            alert(
                "Please select a valid image file."
            );

            input.value = "";

            return;
        }


        // -------------------------------------------------
        // FileReader
        // -------------------------------------------------

        const reader =
            new FileReader();


        reader.onload =
            function (event) {

                previewContainer.innerHTML = "";


                // -----------------------------------------
                // Image
                // -----------------------------------------

                const image =
                    document.createElement("img");

                image.src =
                    event.target.result;

                image.alt =
                    file.name;


                // -----------------------------------------
                // Remove button
                // -----------------------------------------

                const removeButton =
                    document.createElement("button");

                removeButton.type =
                    "button";

                removeButton.className =
                    "single-image-remove";

                removeButton.setAttribute(
                    "aria-label",
                    "Remove image"
                );

                removeButton.innerHTML =
                    '<i class="bi bi-x"></i>';


                // -----------------------------------------
                // Remove image
                // -----------------------------------------

                removeButton.addEventListener(
                    "click",
                    function (event) {

                        event.preventDefault();

                        event.stopPropagation();

                        input.value = "";

                        previewContainer.innerHTML = "";

                        previewContainer.classList.remove(
                            "active"
                        );

                        if (uploadContainer) {

                            uploadContainer.classList.remove(
                                "has-image"
                            );

                        }

                        if (uploadContent) {

                            uploadContent.style.display =
                                "flex";

                        }

                    }
                );


                // -----------------------------------------
                // Add image
                // -----------------------------------------

                previewContainer.appendChild(
                    image
                );


                // -----------------------------------------
                // Add remove button
                // -----------------------------------------

                previewContainer.appendChild(
                    removeButton
                );


                // -----------------------------------------
                // Show preview
                // -----------------------------------------

                previewContainer.classList.add(
                    "active"
                );


                if (uploadContainer) {

                    uploadContainer.classList.add(
                        "has-image"
                    );

                }


                if (uploadContent) {

                    uploadContent.style.display =
                        "none";

                }

            };


        reader.readAsDataURL(file);

    }


    // =====================================================
    // MAIN IMAGE
    // =====================================================

    if (
        mainImageInput &&
        mainImagePreview
    ) {

        mainImageInput.addEventListener(
            "change",
            function () {

                showSingleImagePreview(
                    mainImageInput,
                    mainImagePreview,
                    mainImageUpload,
                    mainUploadContent
                );

            }
        );

    }


    // =====================================================
    // SECONDARY IMAGE
    // =====================================================

    if (
        secondaryImageInput &&
        secondaryImagePreview
    ) {

        secondaryImageInput.addEventListener(
            "change",
            function () {

                showSingleImagePreview(
                    secondaryImageInput,
                    secondaryImagePreview,
                    secondaryImageUpload,
                    secondaryUploadContent
                );

            }
        );

    }


    // =====================================================
    // GALLERY IMAGE SELECTION
    // =====================================================

    if (
        galleryImagesInput &&
        galleryImagesPreview
    ) {

        galleryImagesInput.addEventListener(
            "change",
            function () {

                const files =
                    Array.from(
                        this.files
                    );

                showGalleryImagePreview(
                    files
                );

            }
        );

    }


    // =====================================================
    // SHOW GALLERY IMAGE PREVIEW
    // =====================================================

    function showGalleryImagePreview(
        files
    ) {

        if (!galleryImagesPreview) {
            return;
        }


        // -------------------------------------------------
        // Clear previous preview
        // -------------------------------------------------

        galleryImagesPreview.innerHTML = "";


        // -------------------------------------------------
        // No images
        // -------------------------------------------------

        if (!files.length) {

            if (galleryImageCount) {

                galleryImageCount.textContent =
                    "No gallery images selected.";

            }

            return;
        }


        // -------------------------------------------------
        // Update image count
        // -------------------------------------------------

        if (galleryImageCount) {

            galleryImageCount.textContent =
                `${files.length} image${
                    files.length > 1
                        ? "s"
                        : ""
                } selected.`;

        }


        // -------------------------------------------------
        // Create previews
        // -------------------------------------------------

        files.forEach(
            function (file, index) {

                // -----------------------------------------
                // Skip invalid files
                // -----------------------------------------

                if (
                    !file.type.startsWith("image/")
                ) {

                    return;

                }


                // -----------------------------------------
                // FileReader
                // -----------------------------------------

                const reader =
                    new FileReader();


                reader.onload =
                    function (event) {


                        // ---------------------------------
                        // Preview item
                        // ---------------------------------

                        const previewItem =
                            document.createElement(
                                "div"
                            );

                        previewItem.className =
                            "product-image-preview-item";


                        // ---------------------------------
                        // Image
                        // ---------------------------------

                        const image =
                            document.createElement(
                                "img"
                            );

                        image.src =
                            event.target.result;

                        image.alt =
                            file.name;


                        // ---------------------------------
                        // Remove button
                        // ---------------------------------

                        const removeButton =
                            document.createElement(
                                "button"
                            );

                        removeButton.type =
                            "button";

                        removeButton.className =
                            "remove-product-image";

                        removeButton.setAttribute(
                            "aria-label",
                            "Remove gallery image"
                        );

                        removeButton.innerHTML =
                            '<i class="bi bi-x"></i>';


                        // ---------------------------------
                        // Remove gallery image
                        // ---------------------------------

                        removeButton.addEventListener(
                            "click",
                            function (event) {

                                event.preventDefault();

                                event.stopPropagation();

                                removeGalleryImage(
                                    index
                                );

                            }
                        );


                        // ---------------------------------
                        // Build preview
                        // ---------------------------------

                        previewItem.appendChild(
                            image
                        );

                        previewItem.appendChild(
                            removeButton
                        );


                        // ---------------------------------
                        // Add preview to grid
                        // ---------------------------------

                        galleryImagesPreview.appendChild(
                            previewItem
                        );

                    };


                // -----------------------------------------
                // Read image
                // -----------------------------------------

                reader.readAsDataURL(file);

            }
        );

    }


    // =====================================================
    // REMOVE GALLERY IMAGE
    // =====================================================

    function removeGalleryImage(
        index
    ) {

        if (!galleryImagesInput) {
            return;
        }


        // -------------------------------------------------
        // Get current files
        // -------------------------------------------------

        const files =
            Array.from(
                galleryImagesInput.files
            );


        // -------------------------------------------------
        // Validate index
        // -------------------------------------------------

        if (
            index < 0 ||
            index >= files.length
        ) {
            return;
        }


        // -------------------------------------------------
        // Remove selected file
        // -------------------------------------------------

        files.splice(
            index,
            1
        );


        // -------------------------------------------------
        // Create DataTransfer
        // -------------------------------------------------

        const dataTransfer =
            new DataTransfer();


        // -------------------------------------------------
        // Add remaining files
        // -------------------------------------------------

        files.forEach(
            function (file) {

                dataTransfer.items.add(
                    file
                );

            }
        );


        // -------------------------------------------------
        // Update input
        // -------------------------------------------------

        galleryImagesInput.files =
            dataTransfer.files;


        // -------------------------------------------------
        // Update preview
        // -------------------------------------------------

        showGalleryImagePreview(
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


                    // -------------------------------------
                    // Enable stock input
                    // -------------------------------------

                    if (this.checked) {

                        stockInput.disabled =
                            false;

                        stockInput.focus();

                    }


                    // -------------------------------------
                    // Disable stock input
                    // -------------------------------------

                    else {

                        stockInput.disabled =
                            true;

                        stockInput.value =
                            0;

                    }


                    // -------------------------------------
                    // Update total stock
                    // -------------------------------------

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