from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('collection/<slug:slug>/', views.collection_products, name='collection_products'),
    path('brand/<slug:slug>/', views.brand_products, name='brand_products'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
