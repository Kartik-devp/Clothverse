from django.db import models
from django.urls import reverse

class Collection(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField('image', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('collection_products', args=[self.slug])

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField('logo', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand_products', args=[self.slug])

class Category(models.Model):
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Capitalize first letter of each word
        self.name = ' '.join(word.capitalize() for word in self.name.split())
        super().save(*args, **kwargs)

    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField('image', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_products', args=[self.id])

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField('image')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Capitalize first letter of each word
        self.name = ' '.join(word.capitalize() for word in self.name.split())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def get_all_images(self):
        images = []
        if self.image:
            images.append(self.image)
        images.extend([img.image for img in self.images.all()])
        return images


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('image')
    alt_text = models.CharField(max_length=150, blank=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position', 'id']

    def __str__(self):
        return f"Image for {self.product.name}"

class Size(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
        ('Free Size', 'Free Size'),
    ]

    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    name = models.CharField(max_length=10, choices=SIZE_CHOICES)  # e.g., S, M, L, XL

    def __str__(self):
        return f"{self.name} for {self.product.name}"
