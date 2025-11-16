from django.shortcuts import render
from .models import HomePageProduct

def home(request):
    # Get featured products for home page
    home_products = HomePageProduct.objects.filter(
        is_active=True
    ).select_related('product').order_by('display_order', '-is_featured')[:12]  # Limit to 12 products

    context = {
        'home_products': home_products,
    }
    return render(request, 'core/home.html', context)

def journal(request):
    return render(request, 'core/journal.html')
