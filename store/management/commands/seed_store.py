from django.core.management.base import BaseCommand

from store.models import Brand, Category, Colour, Product, Size


SAMPLE_PRODUCTS = [
    ("Classic Oxford Shirt", "Men", "Zudio", 1499, 20, "Blue", ["M", "L", "XL"], "Cotton", "Regular fit"),
    ("Everyday Crew-Neck T-Shirt", "Men", "Max", 699, 15, "White", ["S", "M", "L", "XL"], "Cotton jersey", "Relaxed fit"),
    ("Slim-Fit Chinos", "Men", "Trends", 1799, 25, "Brown", ["S", "M", "L", "XL"], "Cotton twill", "Slim fit"),
    ("Linen Blend Resort Shirt", "Men", "Zudio", 1599, 10, "White", ["M", "L", "XL"], "Linen blend", "Relaxed fit"),
    ("Urban Zip Hoodie", "Men", "Nike", 2499, 20, "Black", ["S", "M", "L", "XL"], "Cotton fleece", "Regular fit"),
    ("Straight-Leg Denim Jeans", "Men", "Adidas", 2199, 15, "Blue", ["M", "L", "XL", "XXL"], "Denim", "Straight fit"),
    ("Pique Polo T-Shirt", "Men", "Max", 999, 10, "Green", ["S", "M", "L", "XL"], "Cotton pique", "Regular fit"),
    ("Checked Casual Shirt", "Men", "Trends", 1699, 20, "Red", ["M", "L", "XL"], "Cotton", "Regular fit"),
    ("Lightweight Bomber Jacket", "Men", "Nike", 3299, 15, "Black", ["M", "L", "XL"], "Polyester", "Regular fit"),
    ("Everyday Jogger Pants", "Men", "Adidas", 1899, 20, "Grey", ["S", "M", "L", "XL"], "Cotton blend", "Tapered fit"),
    ("Textured Knit Sweater", "Men", "Max", 2299, 25, "Brown", ["M", "L", "XL"], "Acrylic knit", "Regular fit"),
    ("Classic Cotton Kurta", "Men", "Trends", 1399, 10, "Green", ["M", "L", "XL", "XXL"], "Cotton", "Straight fit"),
    ("Graphic Print T-Shirt", "Men", "Zudio", 799, 15, "Black", ["S", "M", "L", "XL"], "Cotton jersey", "Relaxed fit"),
    ("Smart-Casual Blazer", "Men", "Max", 3999, 20, "Grey", ["M", "L", "XL"], "Polyester blend", "Tailored fit"),
    ("Weekend Cargo Trousers", "Men", "Adidas", 2099, 15, "Brown", ["S", "M", "L", "XL"], "Cotton twill", "Relaxed fit"),
    ("Rainbow Stripe T-Shirt", "Kids", "Max", 599, 10, "Blue", ["2Y", "4Y", "6Y", "8Y"], "Cotton jersey", "Easy fit"),
    ("Little Explorer Joggers", "Kids", "Zudio", 799, 15, "Grey", ["2Y", "4Y", "6Y", "8Y"], "Cotton blend", "Pull-on fit"),
    ("Playday Denim Dungarees", "Kids", "Trends", 1299, 20, "Blue", ["2Y", "4Y", "6Y"], "Denim", "Comfort fit"),
    ("Sunny Day Cotton Dress", "Kids", "Max", 999, 10, "Red", ["2Y", "4Y", "6Y", "8Y"], "Cotton", "A-line fit"),
    ("Mini Varsity Hoodie", "Kids", "Nike", 1499, 20, "Navy", ["4Y", "6Y", "8Y", "10Y"], "Cotton fleece", "Regular fit"),
    ("Everyday Polo Shirt", "Kids", "Adidas", 749, 15, "Green", ["2Y", "4Y", "6Y", "8Y"], "Cotton pique", "Regular fit"),
    ("Playful Print Leggings", "Kids", "Max", 549, 10, "Black", ["2Y", "4Y", "6Y", "8Y"], "Cotton stretch", "Stretch fit"),
    ("Soft Flannel Check Shirt", "Kids", "Trends", 899, 15, "Red", ["4Y", "6Y", "8Y", "10Y"], "Cotton flannel", "Easy fit"),
    ("Lightweight Puffer Vest", "Kids", "Nike", 1799, 20, "Blue", ["4Y", "6Y", "8Y", "10Y"], "Polyester", "Layered fit"),
    ("Comfy Pull-On Shorts", "Kids", "Zudio", 499, 10, "Green", ["2Y", "4Y", "6Y", "8Y"], "Cotton jersey", "Relaxed fit"),
    ("Little Star Party Dress", "Kids", "Max", 1199, 15, "Brown", ["2Y", "4Y", "6Y", "8Y"], "Cotton blend", "Flared fit"),
    ("Everyday Cotton Kurta Set", "Kids", "Trends", 1399, 20, "White", ["2Y", "4Y", "6Y", "8Y"], "Cotton", "Straight fit"),
    ("Adventure Cargo Pants", "Kids", "Adidas", 1099, 15, "Brown", ["4Y", "6Y", "8Y", "10Y"], "Cotton twill", "Easy fit"),
    ("Cozy Zip-Up Cardigan", "Kids", "Max", 1299, 10, "Grey", ["2Y", "4Y", "6Y", "8Y"], "Cotton knit", "Regular fit"),
    ("Animal Friends Sleepsuit", "Kids", "Zudio", 699, 10, "White", ["2Y", "4Y", "6Y"], "Organic cotton", "Comfort fit"),
]


class Command(BaseCommand):
    help = "Create the store's base data and 30 example men's and kids' products."

    def handle(self, *args, **kwargs):
        categories = {
            name: Category.objects.get_or_create(name=name)[0]
            for name in ("Men", "Kids")
        }
        brands = {
            name: Brand.objects.get_or_create(name=name)[0]
            for name in ("Zudio", "Max", "Nike", "Adidas", "Trends")
        }
        colour_values = {
            "Black": "#111111",
            "White": "#ffffff",
            "Blue": "#2563eb",
            "Navy": "#1e3a5f",
            "Red": "#dc2626",
            "Green": "#16a34a",
            "Grey": "#6b7280",
            "Brown": "#92400e",
        }
        colours = {
            name: Colour.objects.get_or_create(
                name=name, defaults={"hex_code": hex_code}
            )[0]
            for name, hex_code in colour_values.items()
        }
        size_names = {size for row in SAMPLE_PRODUCTS for size in row[6]}
        sizes = {
            name: Size.objects.get_or_create(name=name)[0]
            for name in size_names
        }

        created_count = 0
        for name, category, brand, price, discount, colour, product_sizes, material, fit in SAMPLE_PRODUCTS:
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": categories[category],
                    "brand": brands[brand],
                    "description": (
                        f"A versatile {name.lower()} designed for comfortable "
                        "everyday wear."
                    ),
                    "material": material,
                    "fit": fit,
                    "care_instructions": "Machine wash cold with similar colours.",
                    "original_price": price,
                    "discount_percent": discount,
                    "stock": 25,
                },
            )
            if created:
                product.colours.add(colours[colour])
                product.sizes.add(*(sizes[size] for size in product_sizes))
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Store data ready. Added {created_count} sample products "
                f"({sum(row[1] == 'Men' for row in SAMPLE_PRODUCTS)} men's, "
                f"{sum(row[1] == 'Kids' for row in SAMPLE_PRODUCTS)} kids')."
            )
        )
