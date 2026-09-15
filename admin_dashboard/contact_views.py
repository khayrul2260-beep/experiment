from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import (
    ContactPage,
    ContactService,
    ContactFAQ,
    ContactSocialLink,
    ContactMessage,
)


# =========================================================
# CONTACT PAGE MANAGEMENT
# =========================================================

def contact_management(request):

    # -----------------------------------------------------
    # GET OR CREATE CONTACT PAGE
    # -----------------------------------------------------

    contact_page = ContactPage.objects.first()

    if contact_page is None:

        contact_page = ContactPage.objects.create(
            hero_eyebrow="CONTACT NAFI",
            hero_title="GET IN TOUCH",
            hero_description=(
                "Have a question, need support, "
                "or want to work with NAFI?"
            ),
            form_button_text="SEND MESSAGE",
            contact_info_title="CONTACT INFORMATION",
            help_title="HOW CAN WE HELP?",
            faq_title="FREQUENTLY ASKED QUESTIONS",
            social_title="STAY CONNECTED",
            final_title="READY TO TALK?",
            final_button_text="CONTACT US",
            final_button_link="/contact/",
        )

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    if request.method == "POST":

        # =================================================
        # MAIN CONTACT
        # =================================================

        contact_page.hero_eyebrow = request.POST.get(
            "hero_eyebrow",
            ""
        ).strip()

        contact_page.hero_title = request.POST.get(
            "hero_title",
            ""
        ).strip()

        contact_page.hero_description = request.POST.get(
            "hero_description",
            ""
        ).strip()

        contact_page.form_button_text = request.POST.get(
            "form_button_text",
            "SEND MESSAGE"
        ).strip()

        # =================================================
        # CONTACT INFORMATION
        # =================================================

        contact_page.contact_info_title = request.POST.get(
            "contact_info_title",
            ""
        ).strip()

        contact_page.email = request.POST.get(
            "email",
            ""
        ).strip()

        contact_page.phone = request.POST.get(
            "phone",
            ""
        ).strip()

        contact_page.whatsapp = request.POST.get(
            "whatsapp",
            ""
        ).strip()

        contact_page.address = request.POST.get(
            "address",
            ""
        ).strip()

        contact_page.support_hours = request.POST.get(
            "support_hours",
            ""
        ).strip()

        # =================================================
        # HOW CAN WE HELP
        # =================================================

        contact_page.help_title = request.POST.get(
            "help_title",
            ""
        ).strip()

        contact_page.help_description = request.POST.get(
            "help_description",
            ""
        ).strip()

        # =================================================
        # FAQ
        # =================================================

        contact_page.faq_title = request.POST.get(
            "faq_title",
            ""
        ).strip()

        # =================================================
        # SOCIAL
        # =================================================

        contact_page.social_title = request.POST.get(
            "social_title",
            ""
        ).strip()

        contact_page.social_description = request.POST.get(
            "social_description",
            ""
        ).strip()

        # =================================================
        # FINAL CTA
        # =================================================

        contact_page.final_title = request.POST.get(
            "final_title",
            ""
        ).strip()

        contact_page.final_description = request.POST.get(
            "final_description",
            ""
        ).strip()

        contact_page.final_button_text = request.POST.get(
            "final_button_text",
            "CONTACT US"
        ).strip()

        contact_page.final_button_link = request.POST.get(
            "final_button_link",
            "/contact/"
        ).strip()

        # =================================================
        # SECTION VISIBILITY
        # =================================================

        contact_page.main_is_active = (
            "main_is_active" in request.POST
        )

        contact_page.info_is_active = (
            "info_is_active" in request.POST
        )

        contact_page.help_is_active = (
            "help_is_active" in request.POST
        )

        contact_page.faq_is_active = (
            "faq_is_active" in request.POST
        )

        contact_page.social_is_active = (
            "social_is_active" in request.POST
        )

        contact_page.final_is_active = (
            "final_is_active" in request.POST
        )

        # =================================================
        # SECTION ORDER
        # =================================================

        def get_order(field_name, default):

            try:
                value = int(
                    request.POST.get(
                        field_name,
                        default
                    )
                )

                if value < 1:
                    return default

                return value

            except (
                ValueError,
                TypeError
            ):

                return default

        contact_page.main_order = get_order(
            "main_order",
            1
        )

        contact_page.info_order = get_order(
            "info_order",
            2
        )

        contact_page.help_order = get_order(
            "help_order",
            3
        )

        contact_page.faq_order = get_order(
            "faq_order",
            4
        )

        contact_page.social_order = get_order(
            "social_order",
            5
        )

        contact_page.final_order = get_order(
            "final_order",
            6
        )

        # =================================================
        # PUBLISHED
        # =================================================

        contact_page.is_published = (
            "is_published" in request.POST
        )

        # =================================================
        # IMAGES
        # =================================================

        desktop_image = request.FILES.get(
            "desktop_image"
        )

        mobile_image = request.FILES.get(
            "mobile_image"
        )

        if desktop_image:
            contact_page.desktop_image = desktop_image

        if mobile_image:
            contact_page.mobile_image = mobile_image

        # =================================================
        # IMAGE ALT
        # =================================================

        contact_page.image_alt = request.POST.get(
            "image_alt",
            ""
        ).strip()

        # =================================================
        # SAVE
        # =================================================

        contact_page.save()

        messages.success(
            request,
            "Contact page updated successfully."
        )

        return redirect(
            "contact_management"
        )

    # -----------------------------------------------------
    # RELATED DATA
    # -----------------------------------------------------

    services = ContactService.objects.filter(
        contact_page=contact_page
    ).order_by(
        "display_order",
        "id"
    )

    faqs = ContactFAQ.objects.filter(
        contact_page=contact_page
    ).order_by(
        "display_order",
        "id"
    )

    social_links = ContactSocialLink.objects.filter(
        contact_page=contact_page
    ).order_by(
        "display_order",
        "id"
    )

    messages_data = ContactMessage.objects.all().order_by(
        "-created_at"
    )

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        "page_title": "Contact Page",

        "contact_page": contact_page,

        "services": services,

        "faqs": faqs,

        "social_links": social_links,

        "messages_data": messages_data,
    }

    # -----------------------------------------------------
    # RENDER
    # -----------------------------------------------------

    return render(
        request,
        "admin_dashboard/contact_management.html",
        context
    )



# =========================================================
# CONTACT SERVICE - ADD
# =========================================================

def add_contact_service(request):

    contact_page = ContactPage.objects.first()

    if contact_page is None:
        messages.error(
            request,
            "Contact Page does not exist."
        )
        return redirect("contact_management")

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        icon = request.POST.get(
            "icon",
            ""
        ).strip()

        try:
            display_order = int(
                request.POST.get(
                    "display_order",
                    1
                )
            )

            if display_order < 1:
                display_order = 1

        except (
            ValueError,
            TypeError
        ):
            display_order = 1

        is_active = (
            "is_active" in request.POST
        )

        if not title:
            messages.error(
                request,
                "Service title is required."
            )
            return redirect(
                "contact_management"
            )

        ContactService.objects.create(
            contact_page=contact_page,
            title=title,
            description=description,
            icon=icon,
            display_order=display_order,
            is_active=is_active,
        )

        messages.success(
            request,
            "Service added successfully."
        )

    return redirect(
        "contact_management"
    )


# =========================================================
# CONTACT SERVICE - UPDATE
# =========================================================

def update_contact_service(request, service_id):

    service = get_object_or_404(
        ContactService,
        id=service_id
    )

    if request.method == "POST":

        service.title = request.POST.get(
            "title",
            ""
        ).strip()

        service.description = request.POST.get(
            "description",
            ""
        ).strip()

        service.icon = request.POST.get(
            "icon",
            ""
        ).strip()

        try:
            display_order = int(
                request.POST.get(
                    "display_order",
                    1
                )
            )

            if display_order < 1:
                display_order = 1

        except (
            ValueError,
            TypeError
        ):
            display_order = 1

        service.display_order = display_order

        service.is_active = (
            "is_active" in request.POST
        )

        if not service.title:
            messages.error(
                request,
                "Service title is required."
            )
            return redirect(
                "contact_management"
            )

        service.save()

        messages.success(
            request,
            "Service updated successfully."
        )

    return redirect(
        "contact_management"
    )


# =========================================================
# CONTACT SERVICE - DELETE
# =========================================================

def delete_contact_service(request, service_id):

    service = get_object_or_404(
        ContactService,
        id=service_id
    )

    if request.method == "POST":

        service.delete()

        messages.success(
            request,
            "Service deleted successfully."
        )

    return redirect(
        "contact_management"
    )



# =========================================================
# CONTACT FAQ - ADD
# =========================================================

def add_contact_faq(request):

    contact_page = ContactPage.objects.first()

    if contact_page is None:
        messages.error(
            request,
            "Contact Page does not exist."
        )
        return redirect(
            "contact_management"
        )

    if request.method == "POST":

        question = request.POST.get(
            "question",
            ""
        ).strip()

        answer = request.POST.get(
            "answer",
            ""
        ).strip()

        try:
            display_order = int(
                request.POST.get(
                    "display_order",
                    1
                )
            )

            if display_order < 1:
                display_order = 1

        except (
            ValueError,
            TypeError
        ):
            display_order = 1

        is_active = (
            "is_active" in request.POST
        )

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not question:
            messages.error(
                request,
                "FAQ question is required."
            )
            return redirect(
                "contact_management"
            )

        if not answer:
            messages.error(
                request,
                "FAQ answer is required."
            )
            return redirect(
                "contact_management"
            )

        # -------------------------------------------------
        # CREATE FAQ
        # -------------------------------------------------

        ContactFAQ.objects.create(
            contact_page=contact_page,
            question=question,
            answer=answer,
            display_order=display_order,
            is_active=is_active,
        )

        messages.success(
            request,
            "FAQ added successfully."
        )

    return redirect(
        "contact_management"
    )


# =========================================================
# CONTACT FAQ - UPDATE
# =========================================================

def update_contact_faq(request, faq_id):

    faq = get_object_or_404(
        ContactFAQ,
        id=faq_id
    )

    if request.method == "POST":

        faq.question = request.POST.get(
            "question",
            ""
        ).strip()

        faq.answer = request.POST.get(
            "answer",
            ""
        ).strip()

        try:
            display_order = int(
                request.POST.get(
                    "display_order",
                    1
                )
            )

            if display_order < 1:
                display_order = 1

        except (
            ValueError,
            TypeError
        ):
            display_order = 1

        faq.display_order = display_order

        faq.is_active = (
            "is_active" in request.POST
        )

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not faq.question:
            messages.error(
                request,
                "FAQ question is required."
            )
            return redirect(
                "contact_management"
            )

        if not faq.answer:
            messages.error(
                request,
                "FAQ answer is required."
            )
            return redirect(
                "contact_management"
            )

        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        faq.save()

        messages.success(
            request,
            "FAQ updated successfully."
        )

    return redirect(
        "contact_management"
    )


# =========================================================
# CONTACT FAQ - DELETE
# =========================================================

def delete_contact_faq(request, faq_id):

    faq = get_object_or_404(
        ContactFAQ,
        id=faq_id
    )

    if request.method == "POST":

        faq.delete()

        messages.success(
            request,
            "FAQ deleted successfully."
        )

    return redirect(
        "contact_management"
    )



# =========================================================
# CONTACT SOCIAL LINK MANAGEMENT
# =========================================================

def add_contact_social_link(request):

    contact_page = ContactPage.objects.first()

    if not contact_page:
        contact_page = ContactPage.objects.create(
            hero_eyebrow="CONTACT NAFI",
            hero_title="GET IN TOUCH",
        )

    if request.method == "POST":

        platform = request.POST.get(
            "platform",
            ""
        ).strip()

        url = request.POST.get(
            "url",
            ""
        ).strip()

        icon = request.POST.get(
            "icon",
            ""
        ).strip()

        display_order = request.POST.get(
            "display_order",
            "1"
        ).strip()

        is_active = (
            request.POST.get("is_active")
            == "on"
        )

        # ==============================================
        # VALIDATION
        # ==============================================

        if not platform:
            messages.error(
                request,
                "Platform name is required."
            )

            return redirect(
                "contact_management"
            )

        if not url:
            messages.error(
                request,
                "Social media URL is required."
            )

            return redirect(
                "contact_management"
            )

        try:
            display_order = int(
                display_order
            )

        except (TypeError, ValueError):

            display_order = 1

        # ==============================================
        # CREATE SOCIAL LINK
        # ==============================================

        ContactSocialLink.objects.create(
            contact_page=contact_page,
            platform=platform,
            url=url,
            icon=icon,
            display_order=display_order,
            is_active=is_active,
        )

        messages.success(
            request,
            "Social link added successfully."
        )

    return redirect(
        "contact_management"
    )


def update_contact_social_link(
    request,
    social_id
):

    social_link = get_object_or_404(
        ContactSocialLink,
        id=social_id
    )

    if request.method == "POST":

        platform = request.POST.get(
            "platform",
            ""
        ).strip()

        url = request.POST.get(
            "url",
            ""
        ).strip()

        icon = request.POST.get(
            "icon",
            ""
        ).strip()

        display_order = request.POST.get(
            "display_order",
            "1"
        ).strip()

        is_active = (
            request.POST.get("is_active")
            == "on"
        )

        # ==============================================
        # VALIDATION
        # ==============================================

        if not platform:
            messages.error(
                request,
                "Platform name is required."
            )

            return redirect(
                "contact_management"
            )

        if not url:
            messages.error(
                request,
                "Social media URL is required."
            )

            return redirect(
                "contact_management"
            )

        try:
            display_order = int(
                display_order
            )

        except (TypeError, ValueError):

            display_order = 1

        # ==============================================
        # UPDATE
        # ==============================================

        social_link.platform = platform
        social_link.url = url
        social_link.icon = icon
        social_link.display_order = display_order
        social_link.is_active = is_active

        social_link.save()

        messages.success(
            request,
            "Social link updated successfully."
        )

    return redirect(
        "contact_management"
    )


def delete_contact_social_link(
    request,
    social_id
):

    social_link = get_object_or_404(
        ContactSocialLink,
        id=social_id
    )

    if request.method == "POST":

        social_link.delete()

        messages.success(
            request,
            "Social link deleted successfully."
        )

    return redirect(
        "contact_management"
    )