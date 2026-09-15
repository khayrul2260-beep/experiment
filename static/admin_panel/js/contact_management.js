/* =========================================================
   NAFI CONTACT MANAGEMENT
   SERVICE + FAQ + SOCIAL
========================================================= */


/* =========================================================
   SERVICE — ADD MODAL
========================================================= */

function openServiceModal() {

    const modal = document.getElementById(
        "serviceModal"
    );

    if (!modal) return;

    modal.classList.add("active");

    document.body.classList.add(
        "contact-modal-open"
    );
}


function closeServiceModal() {

    const modal = document.getElementById(
        "serviceModal"
    );

    if (!modal) return;

    modal.classList.remove("active");

    document.body.classList.remove(
        "contact-modal-open"
    );
}


/* =========================================================
   SERVICE — EDIT MODAL
========================================================= */

function openEditServiceModal(
    id,
    title,
    description,
    icon,
    displayOrder,
    isActive
) {

    const modal = document.getElementById(
        "editServiceModal"
    );

    const form = document.getElementById(
        "editServiceForm"
    );

    if (!modal || !form) return;


    form.action =
        `/admin_dashboard/settings/contact/service/${id}/update/`;


    document.getElementById(
        "edit_service_title"
    ).value = title;


    document.getElementById(
        "edit_service_description"
    ).value = description;


    document.getElementById(
        "edit_service_icon"
    ).value = icon;


    document.getElementById(
        "edit_service_order"
    ).value = displayOrder;


    document.getElementById(
        "edit_service_active"
    ).checked = (
        isActive === "true"
    );


    modal.classList.add("active");

    document.body.classList.add(
        "contact-modal-open"
    );
}


function closeEditServiceModal() {

    const modal = document.getElementById(
        "editServiceModal"
    );

    if (!modal) return;

    modal.classList.remove("active");

    document.body.classList.remove(
        "contact-modal-open"
    );
}


/* =========================================================
   SERVICE — DELETE
========================================================= */

function deleteContactService(
    serviceId
) {

    const confirmed = confirm(
        "Are you sure you want to delete this service?"
    );


    if (!confirmed) {
        return;
    }


    const form = document.createElement(
        "form"
    );

    form.method = "POST";

    form.action =
        `/admin_dashboard/settings/contact/service/${serviceId}/delete/`;


    const csrfTokenElement =
        document.querySelector(
            '[name="csrfmiddlewaretoken"]'
        );


    if (!csrfTokenElement) {
        alert(
            "Security token not found. Please refresh the page."
        );

        return;
    }


    const csrfInput =
        document.createElement(
            "input"
        );

    csrfInput.type = "hidden";

    csrfInput.name =
        "csrfmiddlewaretoken";

    csrfInput.value =
        csrfTokenElement.value;


    form.appendChild(
        csrfInput
    );


    document.body.appendChild(
        form
    );


    form.submit();
}


/* =========================================================
   FAQ — ADD MODAL
========================================================= */

function openFAQModal() {

    const modal = document.getElementById(
        "faqModal"
    );

    if (!modal) return;

    modal.classList.add("active");

    document.body.classList.add(
        "contact-modal-open"
    );
}


function closeFAQModal() {

    const modal = document.getElementById(
        "faqModal"
    );

    if (!modal) return;

    modal.classList.remove("active");

    document.body.classList.remove(
        "contact-modal-open"
    );
}


/* =========================================================
   FAQ — EDIT MODAL
========================================================= */

function openEditFAQModal(
    id,
    question,
    answer,
    displayOrder,
    isActive
) {

    const modal = document.getElementById(
        "editFAQModal"
    );

    const form = document.getElementById(
        "editFAQForm"
    );

    if (!modal || !form) return;


    form.action =
        `/admin_dashboard/settings/contact/faq/${id}/update/`;


    document.getElementById(
        "edit_faq_question"
    ).value = question;


    document.getElementById(
        "edit_faq_answer"
    ).value = answer;


    document.getElementById(
        "edit_faq_order"
    ).value = displayOrder;


    document.getElementById(
        "edit_faq_active"
    ).checked = (
        isActive === "true"
    );


    modal.classList.add("active");

    document.body.classList.add(
        "contact-modal-open"
    );
}


function closeEditFAQModal() {

    const modal = document.getElementById(
        "editFAQModal"
    );

    if (!modal) return;

    modal.classList.remove("active");

    document.body.classList.remove(
        "contact-modal-open"
    );
}


/* =========================================================
   FAQ — DELETE
========================================================= */

function deleteContactFAQ(
    faqId
) {

    const confirmed = confirm(
        "Are you sure you want to delete this FAQ?"
    );


    if (!confirmed) {
        return;
    }


    const form = document.createElement(
        "form"
    );

    form.method = "POST";

    form.action =
        `/admin_dashboard/settings/contact/faq/${faqId}/delete/`;


    const csrfTokenElement =
        document.querySelector(
            '[name="csrfmiddlewaretoken"]'
        );


    if (!csrfTokenElement) {
        alert(
            "Security token not found. Please refresh the page."
        );

        return;
    }


    const csrfInput =
        document.createElement(
            "input"
        );

    csrfInput.type = "hidden";

    csrfInput.name =
        "csrfmiddlewaretoken";

    csrfInput.value =
        csrfTokenElement.value;


    form.appendChild(
        csrfInput
    );


    document.body.appendChild(
        form
    );


    form.submit();
}


/* =========================================================
   SOCIAL — ADD MODAL
========================================================= */

function openSocialModal() {

    const modal = document.getElementById(
        "socialModal"
    );

    if (!modal) return;

    modal.classList.add("active");

    document.body.classList.add(
        "contact-modal-open"
    );
}


function closeSocialModal() {

    const modal = document.getElementById(
        "socialModal"
    );

    if (!modal) return;

    modal.classList.remove("active");

    document.body.classList.remove(
        "contact-modal-open"
    );
}


/* =========================================================
   SOCIAL — EDIT MODAL
========================================================= */

function openEditSocialModal(
    id,
    platform,
    url,
    icon,
    displayOrder,
    isActive
) {

    const modal = document.getElementById(
        "editSocialModal"
    );

    const form = document.getElementById(
        "editSocialForm"
    );

    if (!modal || !form) return;


    form.action =
        `/admin_dashboard/settings/contact/social/${id}/update/`;


    const platformInput =
        document.getElementById(
            "edit_social_platform"
        );

    const urlInput =
        document.getElementById(
            "edit_social_url"
        );

    const iconInput =
        document.getElementById(
            "edit_social_icon"
        );

    const orderInput =
        document.getElementById(
            "edit_social_order"
        );

    const activeInput =
        document.getElementById(
            "edit_social_active"
        );


    if (platformInput) {
        platformInput.value = platform;
    }


    if (urlInput) {
        urlInput.value = url;
    }


    if (iconInput) {
        iconInput.value = icon;
    }


    if (orderInput) {
        orderInput.value = displayOrder;
    }


    if (activeInput) {
        activeInput.checked = (
            isActive === "true"
        );
    }


    modal.classList.add("active");

    document.body.classList.add(
        "contact-modal-open"
    );
}


function closeEditSocialModal() {

    const modal = document.getElementById(
        "editSocialModal"
    );

    if (!modal) return;

    modal.classList.remove("active");

    document.body.classList.remove(
        "contact-modal-open"
    );
}


/* =========================================================
   SOCIAL — DELETE
========================================================= */

function deleteContactSocial(
    socialId
) {

    const confirmed = confirm(
        "Are you sure you want to delete this social link?"
    );


    if (!confirmed) {
        return;
    }


    const form = document.createElement(
        "form"
    );

    form.method = "POST";

    form.action =
        `/admin_dashboard/settings/contact/social/${socialId}/delete/`;


    const csrfTokenElement =
        document.querySelector(
            '[name="csrfmiddlewaretoken"]'
        );


    if (!csrfTokenElement) {
        alert(
            "Security token not found. Please refresh the page."
        );

        return;
    }


    const csrfInput =
        document.createElement(
            "input"
        );

    csrfInput.type = "hidden";

    csrfInput.name =
        "csrfmiddlewaretoken";

    csrfInput.value =
        csrfTokenElement.value;


    form.appendChild(
        csrfInput
    );


    document.body.appendChild(
        form
    );


    form.submit();
}


/* =========================================================
   ALL MODALS — ESCAPE KEY
========================================================= */

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key !== "Escape") {
            return;
        }


        /* SERVICE */

        closeServiceModal();

        closeEditServiceModal();


        /* FAQ */

        closeFAQModal();

        closeEditFAQModal();


        /* SOCIAL */

        closeSocialModal();

        closeEditSocialModal();

    }
);


/* =========================================================
   ALL MODALS — BACKDROP CLICK
========================================================= */

document.addEventListener(
    "click",
    function(event) {

        /* =========================================
           SERVICE
        ========================================== */

        const serviceModal =
            document.getElementById(
                "serviceModal"
            );


        const editServiceModal =
            document.getElementById(
                "editServiceModal"
            );


        if (
            serviceModal &&
            event.target === serviceModal
        ) {

            closeServiceModal();

        }


        if (
            editServiceModal &&
            event.target === editServiceModal
        ) {

            closeEditServiceModal();

        }


        /* =========================================
           FAQ
        ========================================== */

        const faqModal =
            document.getElementById(
                "faqModal"
            );


        const editFAQModal =
            document.getElementById(
                "editFAQModal"
            );


        if (
            faqModal &&
            event.target === faqModal
        ) {

            closeFAQModal();

        }


        if (
            editFAQModal &&
            event.target === editFAQModal
        ) {

            closeEditFAQModal();

        }


        /* =========================================
           SOCIAL
        ========================================== */

        const socialModal =
            document.getElementById(
                "socialModal"
            );


        const editSocialModal =
            document.getElementById(
                "editSocialModal"
            );


        if (
            socialModal &&
            event.target === socialModal
        ) {

            closeSocialModal();

        }


        if (
            editSocialModal &&
            event.target === editSocialModal
        ) {

            closeEditSocialModal();

        }

    }
);