
function openDeleteModal(id,name){

    document.getElementById("deleteOverlay").style.display="flex";

    document.getElementById("productName").innerHTML=name;

    document.getElementById("deleteLink").href="/admin_dashboard/delete/"+id+"/";

}

function closeDeleteModal(){

    document.getElementById("deleteOverlay").style.display="none";
}

