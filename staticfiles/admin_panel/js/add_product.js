const productImageInput =
    document.getElementById("ProductImage");

const productImageUpload =
    document.getElementById("productImageUpload");

const productUploadContent =
    document.getElementById("productUploadContent");

const productPreviewArea =
    document.getElementById("productPreviewArea");

const productPreview =
    document.getElementById("productPreview");

const productFileName =
    document.getElementById("productFileName");


function showProductPreview(file) {

    if (!file) {
        return;
    }

    if (!file.type.startsWith("image/")) {
        return;
    }

    const reader = new FileReader();

    reader.onload = function (event) {

        // Set image
        productPreview.src = event.target.result;

        // Set filename
        productFileName.textContent = file.name;

        // Hide upload content
        productUploadContent.style.display = "none";

        // Show preview
        productPreviewArea.style.display = "block";
    };

    reader.readAsDataURL(file);
}


/* =========================
   FILE SELECT
========================= */

productImageInput.addEventListener(
    "change",
    function () {

        const file = this.files[0];

        showProductPreview(file);
    }
);


/* =========================
   PASTE IMAGE
========================= */

productImageUpload.addEventListener(
    "paste",
    function (event) {

        const items = event.clipboardData.items;

        for (const item of items) {

            if (item.type.startsWith("image/")) {

                const file = item.getAsFile();

                if (!file) {
                    return;
                }

                const dataTransfer =
                    new DataTransfer();

                dataTransfer.items.add(file);

                productImageInput.files =
                    dataTransfer.files;

                showProductPreview(file);

                event.preventDefault();

                break;
            }
        }
    }
);