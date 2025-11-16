from django.db import models
from django.urls import reverse

class HeroBanner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    background_image = models.ImageField('background_image')
    button_text = models.CharField(max_length=50, default='Shop Now')
    button_url = models.CharField(max_length=200, default='/products/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Hero Banner'
        verbose_name_plural = 'Hero Banners'

    def __str__(self):
        return self.title

class FeaturedCollection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    products = models.ManyToManyField('products.Product', related_name='featured_collections')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Featured Collection'
        verbose_name_plural = 'Featured Collections'

    def __str__(self):
        return self.title

class CuratedEdit(models.Model):
    title = models.CharField(max_length=200, help_text="Display title for the curated edit")
    subtitle = models.CharField(max_length=300, blank=True, help_text="Optional subtitle")
    description = models.TextField(blank=True, help_text="Detailed description of the edit")
    image = models.ImageField('image', help_text="Main display image")
    secondary_image = models.ImageField('secondary_image', blank=True, null=True, help_text="Optional secondary image")
    products = models.ManyToManyField('products.Product', related_name='curated_edits', help_text="Products featured in this edit")
    category = models.CharField(max_length=50, choices=[
        ('bestsellers', 'Best Sellers'),
        ('new_arrivals', 'New Arrivals'),
        ('seasonal', 'Seasonal'),
        ('trending', 'Trending Now'),
        ('editor_pick', 'Editor\'s Pick'),
        ('limited_edition', 'Limited Edition'),
    ], default='editor_pick', help_text="Category/type of the curated edit")
    display_order = models.PositiveIntegerField(default=0, help_text="Order in which edits appear (lower numbers first)")
    button_text = models.CharField(max_length=50, default='Shop Now', help_text="Text for the call-to-action button")
    button_url = models.CharField(max_length=200, blank=True, help_text="URL for the call-to-action button (leave blank to auto-generate)")
    is_featured = models.BooleanField(default=False, help_text="Mark as featured edit")
    is_active = models.BooleanField(default=True, help_text="Show this edit on the website")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Curated Edit'
        verbose_name_plural = 'Curated Edits'
        ordering = ['display_order', '-is_featured', '-created_at']

    def __str__(self):
        return self.title

    def get_button_url(self):
        """Return the button URL, or generate one based on category"""
        if self.button_url:
            return self.button_url
        # Auto-generate URL based on category
        if self.category == 'bestsellers':
            return '/products/?sort=bestsellers'
        elif self.category == 'new_arrivals':
            return '/products/?sort=newest'
        elif self.category == 'seasonal':
            return '/products/?season=current'
        else:
            return '/products/'

class JournalPost(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.TextField(blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField('image')
    category = models.CharField(max_length=50, choices=[
        ('style_guide', 'Style Guide'),
        ('sustainability', 'Sustainability'),
        ('trends', 'Trends'),
        ('accessories', 'Accessories'),
        ('history', 'History'),
        ('seasonal', 'Seasonal'),
    ])
    slug = models.SlugField(unique=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Journal Post'
        verbose_name_plural = 'Journal Posts'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('journal_post', args=[self.slug])


class HomePageProduct(models.Model):
    product = models.OneToOneField('products.Product', on_delete=models.CASCADE, related_name='home_page_feature')
    display_title = models.CharField(max_length=200, blank=True, help_text="Custom title for home page (optional)")
    display_description = models.TextField(blank=True, help_text="Custom description for home page (optional)")
    display_order = models.PositiveIntegerField(default=0, help_text="Order of appearance on home page")
    is_featured = models.BooleanField(default=False, help_text="Mark as featured product")
    is_active = models.BooleanField(default=True, help_text="Show on home page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Home Page Product'
        verbose_name_plural = 'Home Page Products'
        ordering = ['display_order', '-is_featured', '-created_at']

    def __str__(self):
        return f"Home Page: {self.product.name}"

    def get_display_title(self):
        return self.display_title or self.product.name

    def get_display_description(self):
        return self.display_description or self.product.description

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'

    def __str__(self):
        return self.email
