from django.contrib import admin
from .models import HeroBanner, FeaturedCollection, CuratedEdit, JournalPost, HomePageProduct, NewsletterSubscription

@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    ordering = ('-is_active', '-created_at')

@admin.register(FeaturedCollection)
class FeaturedCollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    ordering = ('-is_active', '-created_at')
    filter_horizontal = ('products',)

@admin.register(CuratedEdit)
class CuratedEditAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'display_order', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('title', 'subtitle', 'description')
    ordering = ('display_order', '-is_featured', '-created_at')
    filter_horizontal = ('products',)
    prepopulated_fields = {'button_url': ('category',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'description', 'category', 'display_order')
        }),
        ('Images', {
            'fields': ('image', 'secondary_image')
        }),
        ('Products & Links', {
            'fields': ('products', 'button_text', 'button_url')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(JournalPost)
class JournalPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('title', 'excerpt', 'content')
    ordering = ('-is_active', '-created_at')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(HomePageProduct)
class HomePageProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'display_order', 'is_featured', 'is_active', 'created_at')
    list_filter = ('is_featured', 'is_active')
    search_fields = ('product__name', 'display_title', 'display_description')
    ordering = ('display_order', 'product__name')
    raw_id_fields = ('product',)
    fieldsets = (
        ('Product Selection', {
            'fields': ('product',)
        }),
        ('Display Settings', {
            'fields': ('display_title', 'display_description', 'display_order')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
    )

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active',)
    search_fields = ('email',)
    ordering = ('-subscribed_at',)
