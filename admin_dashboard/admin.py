from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ProductsModel)
admin.site.register(Category)

# ---------------------------------------------------------
# BRAND VALUES INLINE
# ---------------------------------------------------------

class AboutValueInline(admin.TabularInline):
    model = AboutValue
    extra = 1
    fields = (
        "title",
        "description",
        "icon",
        "display_order",
        "is_active",
    )


# ---------------------------------------------------------
# QUALITY COMMITMENTS INLINE
# ---------------------------------------------------------

class AboutQualityInline(admin.TabularInline):
    model = AboutQuality
    extra = 1
    fields = (
        "title",
        "description",
        "icon",
        "display_order",
        "is_active",
    )


# ---------------------------------------------------------
# BRAND JOURNEY INLINE
# ---------------------------------------------------------

class AboutJourneyInline(admin.TabularInline):
    model = AboutJourney
    extra = 1
    fields = (
        "year",
        "title",
        "description",
        "image",
        "display_order",
        "is_active",
    )


# ---------------------------------------------------------
# ABOUT PAGE ADMIN
# ---------------------------------------------------------

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "hero_title",
        "is_published",
        "updated_at",
    )

    list_filter = (
        "is_published",
    )

    search_fields = (
        "hero_title",
        "who_title",
        "origin_title",
        "vision_title",
    )

    readonly_fields = (
        "updated_at",
    )

    inlines = [
        AboutValueInline,
        AboutQualityInline,
        AboutJourneyInline,
    ]

    fieldsets = (

        # HERO
        (
            "Hero Section",
            {
                "fields": (
                    "hero_eyebrow",
                    "hero_title",
                    "hero_description",
                    "hero_image",
                )
            },
        ),

        # WHO WE ARE
        (
            "Who We Are",
            {
                "fields": (
                    "who_title",
                    "who_content",
                    "who_image",
                )
            },
        ),

        # ORIGIN
        (
            "Brand Origin",
            {
                "fields": (
                    "origin_title",
                    "origin_content",
                )
            },
        ),

        # VISION
        (
            "Vision",
            {
                "fields": (
                    "vision_title",
                    "vision_statement",
                    "vision_content",
                )
            },
        ),

        # MODERN MAN
        (
            "Made for the Modern Man",
            {
                "fields": (
                    "modern_title",
                    "modern_content",
                )
            },
        ),

        # AESTHETIC
        (
            "NAFI Aesthetic",
            {
                "fields": (
                    "aesthetic_title",
                    "aesthetic_content",
                    "aesthetic_image",
                )
            },
        ),

        # QUALITY
        (
            "Quality",
            {
                "fields": (
                    "quality_title",
                    "quality_intro",
                )
            },
        ),

        # TRANSPARENCY
        (
            "Transparency",
            {
                "fields": (
                    "transparency_title",
                    "transparency_content",
                )
            },
        ),

        # WHY NAFI
        (
            "Why NAFI",
            {
                "fields": (
                    "why_title",
                    "why_content",
                )
            },
        ),

        # PROFILE
        (
            "NAFI at a Glance",
            {
                "fields": (
                    "profile_title",
                    "profile_category",
                    "profile_focus",
                    "profile_style",
                    "profile_values",
                    "profile_products",
                )
            },
        ),

        # FINAL CTA
        (
            "Final Brand Statement",
            {
                "fields": (
                    "final_title",
                    "final_content",
                    "final_statement",
                    "cta_text",
                    "final_image",
                )
            },
        ),

        # STATUS
        (
            "Publishing",
            {
                "fields": (
                    "is_published",
                    "updated_at",
                )
            },
        ),
    )