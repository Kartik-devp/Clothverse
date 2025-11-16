from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from products.models import Category, Product


class Command(BaseCommand):
    help = (
        "Delete all products that belong to a specific category. "
        "Identify the category by --name, --slug, or --id. "
        "Optionally also delete the category with --delete-category."
    )

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--name", type=str, help="Category name")
        group.add_argument("--slug", type=str, help="Category slug")
        group.add_argument("--id", type=int, help="Category ID")

        parser.add_argument(
            "--delete-category",
            action="store_true",
            help="Also delete the Category after deleting its products",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without applying changes",
        )

    def _get_category(self, name=None, slug=None, id=None):  # noqa: A002 - id name ok in CLI
        if name is not None:
            return Category.objects.filter(name=name).first()
        if slug is not None:
            return Category.objects.filter(slug=slug).first()
        if id is not None:
            return Category.objects.filter(id=id).first()
        return None

    def handle(self, *args, **options):
        name = options.get("name")
        slug = options.get("slug")
        category_id = options.get("id")
        delete_category = options.get("delete_category")
        dry_run = options.get("dry_run")

        category = self._get_category(name=name, slug=slug, id=category_id)
        if not category:
            ident = (
                f"name='{name}'" if name is not None else (
                    f"slug='{slug}'" if slug is not None else f"id={category_id}"
                )
            )
            raise CommandError(f"Category not found for {ident}")

        qs = Product.objects.filter(category=category)
        product_count = qs.count()

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - no changes will be made"))
        self.stdout.write(
            f"Category: {category} (id={category.id}, slug={getattr(category, 'slug', '')})"
        )
        self.stdout.write(f"Products to delete: {product_count}")

        if dry_run:
            if delete_category:
                self.stdout.write("Category would also be deleted.")
            return

        with transaction.atomic():
            deleted = qs.delete()
            # deleted is a tuple: (num_deleted, {model_label: count, ...})
            self.stdout.write(self.style.SUCCESS(f"Deleted products result: {deleted[0]} rows"))

            if delete_category:
                category_repr = str(category)
                category_id_val = category.id
                category.delete()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Deleted category '{category_repr}' (id={category_id_val})"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Done."))


