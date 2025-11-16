from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Collection, Brand

def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories
    })

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_active=True)
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category
    })

def collection_products(request, slug):
    collection = get_object_or_404(Collection, slug=slug, is_active=True)
    products = Product.objects.filter(collection=collection, is_active=True)
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_collection': collection
    })

def brand_products(request, slug):
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    products = Product.objects.filter(brand=brand, is_active=True)
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_brand': brand
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    categories = Category.objects.all()
    return render(request, 'products/product_detail.html', {
        'product': product,
        'categories': categories,
    })
