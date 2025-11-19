from django.contrib import admin
from .models import Category, Product, ProductImage, Size
import cloudinary
import cloudinary.uploader
from django import forms
from django.contrib import messages

# Register your models here.

#------------------------Category Admin--------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = ('name',)
    ordering = ('id',)
    exclude = ('description', 'image')

#-----------------------Product Admin----------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','price','category','image')
    list_filter = ('category',)
    search_fields = ('name','description')
    ordering = ('id',)
    exclude = ('collection', 'brand')

    class ProductImageInline(admin.TabularInline):
        model = ProductImage
        extra = 3
    class SizeInline(admin.TabularInline):
        model = Size
        extra = 6  # Show all 6 sizes by default
        max_num = 6  # Limit to 6 sizes max
    inlines = [ProductImageInline, SizeInline]

    def save_model(self, request, obj, form, change):
        # Upload image to Cloudinary if a new image is provided
        if obj.image and not isinstance(obj.image, str):
            try:
                result = cloudinary.uploader.upload(obj.image.path, folder='products')
                obj.image = result['url']
            except Exception as e:
                messages.error(request, f"Failed to upload image to Cloudinary: {e}")
                obj.image = ''  # Set to empty string if upload fails
        super().save_model(request, obj, form, change)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id','product','position')
    list_filter = ('product',)

    def save_model(self, request, obj, form, change):
        # Upload image to Cloudinary if a new image is provided
        if obj.image and not isinstance(obj.image, str):
            try:
                result = cloudinary.uploader.upload(obj.image.path, folder='products')
                obj.image = result['url']
            except Exception as e:
                messages.error(request, f"Failed to upload image to Cloudinary: {e}")
                obj.image = ''  # Set to empty string if upload fails
        super().save_model(request, obj, form, change)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id','product','name')
    list_filter = ('product',)
