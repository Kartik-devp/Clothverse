import os
import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files import File
from django.conf import settings

from products.models import Category, Product, ProductImage


CATEGORIES = [
    "Men",
    "Women",
    "Kids",
    "Tops",
    "Bottoms",
    "Dresses",
    "Outerwear",
    "Accessories",
]

PRODUCT_ADJECTIVES = [
    "Classic",
    "Premium",
    "Essential",
    "Modern",
    "Relaxed",
    "Athletic",
    "Vintage",
    "Elegant",
    "Street",
    "Casual",
]

PRODUCT_ITEMS = [
    "T-Shirt",
    "Shirt",
    "Jeans",
    "Chinos",
    "Hoodie",
    "Jacket",
    "Skirt",
    "Dress",
    "Shorts",
    "Sweater",
]

PLACEHOLDER_FILES = ["4K_professional_studio_photo_of-1.jpg", "4K_professional_studio_photo_of-2.jpg", "4K_professional_studio_photo_of-3.jpg", "test_image_0.jpg"]


class Command(BaseCommand):
    help = "Seed database with 150 clothing products across categories, each with 4 images"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=150, help="Number of products to create")
        parser.add_argument("--clear", action="store_true", help="Clear existing products and categories before seeding (danger)")

    def handle(self, *args, **options):
        count = options["count"]
        clear = options["clear"]

        if clear:
            self.stdout.write(self.style.WARNING("Clearing existing products (and images) and categories..."))
            ProductImage.objects.all().delete()
            Product.objects.all().delete()
            # Do not delete categories if they may be referenced elsewhere. Remove comment if you want to clear.
            # Category.objects.all().delete()

        # Ensure categories
        categories = []
        for name in CATEGORIES:
            cat, _ = Category.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            if not cat.slug:
                cat.slug = slugify(name)
                cat.save(update_fields=["slug"])
            categories.append(cat)

        # Resolve placeholder image paths
        media_images_dir = os.path.join(settings.BASE_DIR, "media")
        placeholder_paths = []
        for fname in PLACEHOLDER_FILES:
            path = os.path.join(media_images_dir, fname)
            if not os.path.exists(path):
                self.stdout.write(self.style.WARNING(f"Placeholder not found: {path}. Using first available if any."))
            else:
                placeholder_paths.append(path)

        created = 0
        for i in range(count):
            # Build product name and slug
            cat = random.choice(categories)
            name = f"{random.choice(PRODUCT_ADJECTIVES)} {random.choice(PRODUCT_ITEMS)} {random.randint(1000, 9999)}"
            base_slug = slugify(name)
            slug = base_slug
            n = 1
            while Product.objects.filter(slug=slug).exists():
                n += 1
                slug = f"{base_slug}-{n}"

            price = round(random.uniform(9.99, 149.99), 2)
            description = (
                "A stylish and comfortable piece perfect for everyday wear. "
                "Crafted with quality materials for durability and comfort."
            )

            product = Product(
                category=cat,
                name=name,
                slug=slug,
                description=description,
                price=price,
                is_active=True,
            )
            # Attach a main image from placeholders if present
            main_path = random.choice(placeholder_paths) if placeholder_paths else None
            if main_path and os.path.exists(main_path):
                with open(main_path, "rb") as f:
                    product.image.save(os.path.basename(main_path), File(f), save=False)

            product.save()

            # Add 4 side images
            used = random.sample(placeholder_paths, k=min(4, len(placeholder_paths))) if placeholder_paths else []
            pos = 0
            for p in used:
                if not os.path.exists(p):
                    continue
                img = ProductImage(product=product, position=pos)
                with open(p, "rb") as f:
                    img.image.save(os.path.basename(p), File(f), save=False)
                img.save()
                pos += 1

            created += 1
            if created % 25 == 0:
                self.stdout.write(self.style.SUCCESS(f"Created {created}/{count} products..."))

        self.stdout.write(self.style.SUCCESS(f"Seeding complete. Created {created} products."))
