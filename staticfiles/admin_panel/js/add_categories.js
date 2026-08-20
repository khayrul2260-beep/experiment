const imageInput =
    document.getElementById("categoryImage");

const uploadContent =
    document.getElementById("uploadContent");

const previewBox =
    document.getElementById("imagePreview");

const previewImage =
    document.getElementById("previewImage");

const fileName =
    document.getElementById("fileName");


imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        return;
    }

    if (!file.type.startsWith("image/")) {
        return;
    }


    const reader = new FileReader();


    reader.onload = function (e) {

        // Image
        previewImage.src = e.target.result;


        // File name
        fileName.textContent = file.name;


        // Hide upload content
        uploadContent.style.display = "none";


        // Show preview
        previewBox.style.display = "flex";
    };


    reader.readAsDataURL(file);

});