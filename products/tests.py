from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category, Brand, ProductImage

class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Test Brand')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=100.00,
            category=self.category,
            brand=self.brand
        )
        # Create 5 images for the product
        for i in range(5):
            ProductImage.objects.create(product=self.product, image=f'test_image_{i}.jpg')

    def test_product_detail_view_shows_5_images(self):
        response = self.client.get(reverse('product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'thumbnail', count=5)