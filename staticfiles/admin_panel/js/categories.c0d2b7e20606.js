function openCategoryDeleteModal(id, name) {

    document.getElementById("categoryDeleteOverlay").style.display = "flex";

    document.getElementById("categoryName").innerHTML = name;

    document.getElementById("categoryDeleteLink").href = "/admin_dashboard/categories/delete/" + id + "/";
}


function closeCategoryDeleteModal() {

    document.getElementById("categoryDeleteOverlay").style.display = "none";
}