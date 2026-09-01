document.addEventListener("DOMContentLoaded", function () {

    // ==========================================================
    // EDIT PRODUCT - IMAGE MANAGEMENT
    // ==========================================================

    const productForm = document.querySelector(
        ".product-form-card form"
    );


    // ==========================================================
    // HELPER
    // ==========================================================

    function isValidImage(file) {

        return (
            file &&
            file.type &&
            file.type.startsWith("image/")
        );

    }


    function createObjectURL(file) {

        return URL.createObjectURL(file);

    }


    // ==========================================================
    // MAIN IMAGE
    // ==========================================================

    const mainImageBox =
        document.getElementById("mainImageBox");

    const mainImageInput =
        document.getElementById("mainImageInput");


    if (
        mainImageBox &&
        mainImageInput
    ) {

        mainImageBox.addEventListener(
            "click",
            function () {

                mainImageInput.click();

            }
        );


        mainImageInput.addEventListener(
            "change",
            function () {

                const file =
                    this.files[0];


                if (!file) {
                    return;
                }


                if (!isValidImage(file)) {

                    alert(
                        "Please select a valid image."
                    );

                    this.value = "";

                    return;

                }


                let preview =
                    document.getElementById(
                        "mainImagePreview"
                    );


                const imageURL =
                    createObjectURL(file);


                // Existing preview
                if (preview) {

                    preview.src =
                        imageURL;

                }


                // Empty state
                else {

                    mainImageBox.innerHTML = "";


                    preview =
                        document.createElement("img");


                    preview.id =
                        "mainImagePreview";


                    preview.src =
                        imageURL;


                    preview.alt =
                        "Main Image";


                    mainImageBox.appendChild(
                        preview
                    );


                    /*
                     * IMPORTANT
                     *
                     * Do NOT create another input.
                     *
                     * The original mainImageInput
                     * already contains the selected file.
                     */

                    mainImageBox.appendChild(
                        mainImageInput
                    );

                }

            }
        );

    }



    // ==========================================================
    // SECONDARY IMAGE
    // ==========================================================

    const secondaryImageBox =
        document.getElementById(
            "secondaryImageBox"
        );


    const secondaryImageInput =
        document.getElementById(
            "secondaryImageInput"
        );


    if (
        secondaryImageBox &&
        secondaryImageInput
    ) {

        secondaryImageBox.addEventListener(
            "click",
            function () {

                secondaryImageInput.click();

            }
        );


        secondaryImageInput.addEventListener(
            "change",
            function () {

                const file =
                    this.files[0];


                if (!file) {
                    return;
                }


                if (!isValidImage(file)) {

                    alert(
                        "Please select a valid image."
                    );

                    this.value = "";

                    return;

                }


                let preview =
                    document.getElementById(
                        "secondaryImagePreview"
                    );


                const imageURL =
                    createObjectURL(file);


                // Existing image
                if (preview) {

                    preview.src =
                        imageURL;

                }


                // Empty state
                else {

                    secondaryImageBox.innerHTML =
                        "";


                    preview =
                        document.createElement(
                            "img"
                        );


                    preview.id =
                        "secondaryImagePreview";


                    preview.src =
                        imageURL;


                    preview.alt =
                        "Secondary Image";


                    secondaryImageBox.appendChild(
                        preview
                    );


                    /*
                     * Keep original file input.
                     */
                    secondaryImageBox.appendChild(
                        secondaryImageInput
                    );

                }

            }
        );

    }



    // ==========================================================
    // GALLERY ELEMENTS
    // ==========================================================

    const galleryContainer =
        document.getElementById(
            "galleryImagesContainer"
        );


    const galleryInput =
        document.getElementById(
            "galleryImageInput"
        );


    const addGalleryButton =
        document.getElementById(
            "addGalleryImageBtn"
        );



    /*
     * This DataTransfer is VERY IMPORTANT.
     *
     * It represents the actual files that will finally
     * be submitted to Django as:
     *
     * request.FILES.getlist("gallery_images")
     */

    let galleryFiles =
        new DataTransfer();



    // ==========================================================
    // INITIAL GALLERY FILES
    // ==========================================================

    if (galleryInput) {

        /*
         * Normally empty when page loads.
         *
         * We keep it as the actual submission input.
         */

        galleryFiles =
            new DataTransfer();

    }



    // ==========================================================
    // ADD GALLERY BUTTON
    // ==========================================================

    if (
        addGalleryButton &&
        galleryInput &&
        galleryContainer
    ) {

        addGalleryButton.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                galleryInput.click();

            }
        );


        galleryInput.addEventListener(
            "change",
            function () {

                const selectedFiles =
                    Array.from(
                        this.files
                    );


                if (!selectedFiles.length) {
                    return;
                }


                selectedFiles.forEach(
                    function (file) {

                        if (
                            !isValidImage(file)
                        ) {

                            return;

                        }


                        /*
                         * Add file to the actual
                         * DataTransfer collection.
                         */

                        galleryFiles.items.add(
                            file
                        );

                    }
                );


                /*
                 * Put DataTransfer files back
                 * into the real input.
                 */

                galleryInput.files =
                    galleryFiles.files;


                /*
                 * Render newly selected images.
                 */

                renderNewGalleryImages();


                /*
                 * Remove empty state.
                 */

                const emptyState =
                    document.getElementById(
                        "galleryEmptyState"
                    );


                if (emptyState) {

                    emptyState.remove();

                }

            }
        );

    }



    // ==========================================================
    // RENDER NEW GALLERY IMAGES
    // ==========================================================

    function renderNewGalleryImages() {

        if (!galleryContainer) {
            return;
        }


        /*
         * Remove only dynamically created
         * new gallery items.
         *
         * Existing database images remain untouched.
         */

        galleryContainer
            .querySelectorAll(
                ".gallery-new-item"
            )
            .forEach(
                function (item) {

                    item.remove();

                }
            );


        const files =
            Array.from(
                galleryFiles.files
            );


        files.forEach(
            function (file, index) {

                createNewGalleryItem(
                    file,
                    index
                );

            }
        );

    }



    // ==========================================================
    // CREATE NEW GALLERY ITEM
    // ==========================================================

    function createNewGalleryItem(
        file,
        fileIndex
    ) {

        const item =
            document.createElement("div");


        item.className =
            "gallery-image-item gallery-new-item";


        item.dataset.fileIndex =
            fileIndex;


        const wrapper =
            document.createElement("div");


        wrapper.className =
            "gallery-image-wrapper";


        const image =
            document.createElement("img");


        image.src =
            createObjectURL(file);


        image.alt =
            file.name;


        const controls =
            document.createElement("div");


        controls.className =
            "gallery-image-controls";


        // ======================================================
        // CHANGE BUTTON
        // ======================================================

        const changeButton =
            document.createElement("button");


        changeButton.type =
            "button";


        changeButton.className =
            "gallery-change-btn";


        changeButton.title =
            "Change image";


        changeButton.textContent =
            "✏";


        // Hidden input for changing NEW file
        const changeInput =
            document.createElement("input");


        changeInput.type =
            "file";


        changeInput.accept =
            "image/*";


        changeInput.hidden =
            true;


        changeButton.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                event.stopPropagation();

                changeInput.click();

            }
        );


        changeInput.addEventListener(
            "change",
            function () {

                const newFile =
                    this.files[0];


                if (!newFile) {
                    return;
                }


                if (!isValidImage(newFile)) {

                    alert(
                        "Please select a valid image."
                    );

                    this.value = "";

                    return;

                }


                /*
                 * Replace the actual file inside
                 * DataTransfer.
                 */

                replaceNewGalleryFile(
                    fileIndex,
                    newFile
                );

            }
        );



        // ======================================================
        // DELETE BUTTON
        // ======================================================

        const deleteButton =
            document.createElement("button");


        deleteButton.type =
            "button";


        deleteButton.className =
            "gallery-delete-btn";


        deleteButton.title =
            "Delete image";


        deleteButton.textContent =
            "🗑";


        deleteButton.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                event.stopPropagation();


                const confirmed =
                    confirm(
                        "Are you sure you want to delete this image?"
                    );


                if (!confirmed) {
                    return;
                }


                removeNewGalleryFile(
                    fileIndex
                );

            }
        );


        controls.appendChild(
            changeButton
        );


        controls.appendChild(
            deleteButton
        );


        wrapper.appendChild(
            image
        );


        wrapper.appendChild(
            controls
        );


        item.appendChild(
            wrapper
        );


        item.appendChild(
            changeInput
        );


        galleryContainer.appendChild(
            item
        );

    }



    // ==========================================================
    // REPLACE NEW GALLERY FILE
    // ==========================================================

    function replaceNewGalleryFile(
        index,
        newFile
    ) {

        const files =
            Array.from(
                galleryFiles.files
            );


        if (
            index < 0 ||
            index >= files.length
        ) {

            return;

        }


        files[index] =
            newFile;


        const newDataTransfer =
            new DataTransfer();


        files.forEach(
            function (file) {

                newDataTransfer.items.add(
                    file
                );

            }
        );


        galleryFiles =
            newDataTransfer;


        galleryInput.files =
            galleryFiles.files;


        renderNewGalleryImages();

    }



    // ==========================================================
    // REMOVE NEW GALLERY FILE
    // ==========================================================

    function removeNewGalleryFile(
        index
    ) {

        const files =
            Array.from(
                galleryFiles.files
            );


        if (
            index < 0 ||
            index >= files.length
        ) {

            return;

        }


        files.splice(
            index,
            1
        );


        const newDataTransfer =
            new DataTransfer();


        files.forEach(
            function (file) {

                newDataTransfer.items.add(
                    file
                );

            }
        );


        galleryFiles =
            newDataTransfer;


        galleryInput.files =
            galleryFiles.files;


        renderNewGalleryImages();


        /*
         * If there are no images left,
         * show empty state.
         */

        const existingImages =
            galleryContainer.querySelectorAll(
                ".gallery-image-item:not(.gallery-new-item)"
            );


        if (
            files.length === 0 &&
            existingImages.length === 0
        ) {

            showGalleryEmptyState();

        }

    }



    // ==========================================================
    // EXISTING DATABASE GALLERY IMAGES
    // ==========================================================

    const existingGalleryItems =
        document.querySelectorAll(
            ".gallery-image-item:not(.gallery-new-item)"
        );


    existingGalleryItems.forEach(
        function (item) {

            const changeButton =
                item.querySelector(
                    ".gallery-change-btn"
                );


            const changeInput =
                item.querySelector(
                    ".gallery-change-input"
                );


            const deleteButton =
                item.querySelector(
                    ".gallery-delete-btn"
                );


            const deleteInput =
                item.querySelector(
                    ".delete-image-input"
                );


            const image =
                item.querySelector(
                    ".gallery-image-wrapper img"
                );


            const imageId =
                item.dataset.imageId;



            // ==================================================
            // EXISTING IMAGE - CHANGE
            // ==================================================
            // ==========================================================
            // EXISTING IMAGE - CHANGE / REPLACE
            // ==========================================================

            if (
                changeButton &&
                changeInput &&
                image
            ) {
            
                changeInput.name =
                    "gallery_replace_files[]";
            
            
                // ------------------------------------------
                // Replacement ID input
                // ------------------------------------------
            
                let replaceIdInput =
                    item.querySelector(
                        ".gallery-replace-id-input"
                    );
                
                
                if (!replaceIdInput) {
                
                    replaceIdInput =
                        document.createElement(
                            "input"
                        );
                    
                    replaceIdInput.type =
                        "hidden";
                    
                    replaceIdInput.className =
                        "gallery-replace-id-input";
                    
                    replaceIdInput.name =
                        "gallery_replace_ids[]";
                    
                    replaceIdInput.value =
                        imageId;
                    
                    replaceIdInput.disabled =
                        true;
                    
                    item.appendChild(
                        replaceIdInput
                    );
                }
            
            
                // ------------------------------------------
                // Change button
                // ------------------------------------------
            
                changeButton.addEventListener(
                    "click",
                    function (event) {
                    
                        event.preventDefault();
                        event.stopPropagation();
                    
                        changeInput.click();
                    
                    }
                );
            
            
                // ------------------------------------------
                // New file selected
                // ------------------------------------------
            
                changeInput.addEventListener(
                    "change",
                    function () {
                    
                        const file =
                            this.files[0];
                    
                    
                        if (!file) {
                            return;
                        }
                    
                    
                        if (
                            !isValidImage(file)
                        ) {
                        
                            alert(
                                "Please select a valid image."
                            );
                        
                            this.value = "";
                        
                            return;
                        }
                    
                    
                        // ----------------------------------
                        // Preview new image
                        // ----------------------------------
                    
                        image.src =
                            createObjectURL(
                                file
                            );
                        
                        
                        // ----------------------------------
                        // Enable replacement data
                        // ----------------------------------
                        
                        this.disabled =
                            false;
                        
                        
                        replaceIdInput.disabled =
                            false;
                        
                        
                        replaceIdInput.value =
                            imageId;
                        
                        
                        item.dataset.replaced =
                            "true";
                        
                    }
                );
            
            }



            // ==================================================
            // EXISTING IMAGE - DELETE
            // ==================================================

            if (deleteButton) {

                deleteButton.addEventListener(
                    "click",
                    function (event) {

                        event.preventDefault();

                        event.stopPropagation();


                        const confirmed =
                            confirm(
                                "Are you sure you want to delete this image?"
                            );


                        if (!confirmed) {
                            return;
                        }


                        if (deleteInput) {

                            deleteInput.disabled =
                                false;

                        }

                        const replaceInput =
                            item.querySelector(
                                ".gallery-change-input"
                            );
                        
                        
                        const replaceIdInput =
                            item.querySelector(
                                ".gallery-replace-id-input"
                            );
                        
                        
                        if (replaceInput) {
                        
                            replaceInput.disabled =
                                true;
                        
                            replaceInput.value =
                                "";
                        
                        }


                        if (replaceIdInput) {
                        
                            replaceIdInput.disabled =
                                true;
                        
                        }

                        item.dataset.deleted =
                            "true";


                        item.style.display =
                            "none";

                    }
                );

            }

        }
    );



    // ==========================================================
    // EMPTY GALLERY STATE
    // ==========================================================

    function showGalleryEmptyState() {

        if (!galleryContainer) {
            return;
        }


        if (
            document.getElementById(
                "galleryEmptyState"
            )
        ) {

            return;

        }


        const emptyState =
            document.createElement("div");


        emptyState.id =
            "galleryEmptyState";


        emptyState.className =
            "gallery-empty-state";


        emptyState.innerHTML = `

            <div class="empty-gallery-icon">
                +
            </div>

            <p>
                No gallery images yet
            </p>

            <span>
                Click "Add Image" to upload gallery images.
            </span>

        `;


        galleryContainer.appendChild(
            emptyState
        );

    }



    // ==========================================================
    // SIZE & STOCK MANAGEMENT
    // ==========================================================

    const sizeToggles =
        document.querySelectorAll(
            ".size-toggle"
        );


    const totalStockElement =
        document.getElementById(
            "totalStock"
        );


    const totalStockInput =
        document.getElementById(
            "ProductStock"
        );



    // ==========================================================
    // UPDATE TOTAL STOCK
    // ==========================================================

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
                                input.value,
                                10
                            ) || 0;

                    }

                }
            );


        if (totalStockElement) {

            totalStockElement.textContent =
                total;

        }


        /*
         * ProductStock is readonly,
         * but it must contain the calculated
         * value when form is submitted.
         */

        if (totalStockInput) {

            totalStockInput.value =
                total;

        }

    }



    // ==========================================================
    // SIZE CHECKBOX
    // ==========================================================

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


                    if (this.checked) {

                        stockInput.disabled =
                            false;

                    }

                    else {

                        stockInput.disabled =
                            true;

                        stockInput.value =
                            0;

                    }


                    updateTotalStock();

                }
            );

        }
    );



    // ==========================================================
    // STOCK INPUT CHANGE
    // ==========================================================

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



    // ==========================================================
    // INITIAL STOCK
    // ==========================================================

    updateTotalStock();



    // ==========================================================
    // FORM SUBMIT
    // ==========================================================

    if (productForm) {

        productForm.addEventListener(
            "submit",
            function () {

                /*
                 * Make absolutely sure the current
                 * DataTransfer files are attached
                 * to the real form input.
                 */

                if (galleryInput) {

                    galleryInput.files =
                        galleryFiles.files;

                }


                /*
                 * Update total stock one last time
                 * before Django receives the form.
                 */

                updateTotalStock();

            }
        );

    }

});