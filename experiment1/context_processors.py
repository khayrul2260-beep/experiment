from admin_dashboard.models import Category


def navbar_categories(request):

    categories = Category.objects.filter(
        is_active=True
    ).order_by("created_at")

    return {
        "navbar_categories": categories
    }