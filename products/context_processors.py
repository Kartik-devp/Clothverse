from django.urls import reverse

def shop_menu_items(request):
    """
    Provides the navigation menu items to all templates.
    """
    return {
        'shop_menu_items': {
            "shop": [
                {"name": "Home", "url": reverse("home"), "has_dropdown": False},
                {"name": "Shop", "url": reverse("product_list"), "has_dropdown": True},
                {"name": "New Arrivals", "url": reverse("product_list") + "?sort=newest", "has_dropdown": True},
                {"name": "Collections", "url": "#", "has_dropdown": True},
                {"name": "Journal", "url": reverse("journal"), "has_dropdown": False},
            ]
        }
    }