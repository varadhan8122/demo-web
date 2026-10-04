from decimal import Decimal
from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.name

class Brand(models.Model):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self): return self.name

class Colour(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(max_length=7, default="#000000")
    def __str__(self): return self.name

class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self): return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    material = models.CharField(max_length=100, blank=True)
    fit = models.CharField(max_length=100, blank=True)
    care_instructions = models.TextField(blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    colours = models.ManyToManyField(Colour, blank=True)
    sizes = models.ManyToManyField(Size, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def selling_price(self):
        return (self.original_price * (Decimal(100) - Decimal(self.discount_percent)) / Decimal(100)).quantize(Decimal("0.01"))

    def __str__(self): return self.name

class ProductColourImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colour_images")
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/colours/")
    class Meta:
        unique_together = ("product", "colour")

class Order(models.Model):
    STATUS = [("PENDING","Pending"),("CONFIRMED","Confirmed"),("PROCESSING","Processing"),
              ("SHIPPED","Shipped"),("DELIVERED","Delivered"),("CANCELLED","Cancelled")]
    PAYMENT = [("COD","Cash on Delivery"),("UPI","UPI"),("CARD","Card"),("NETBANKING","Net Banking")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    order_id = models.CharField(max_length=24, unique=True)
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    pincode = models.CharField(max_length=10)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT, default="COD")
    payment_status = models.CharField(max_length=20, default="PENDING")
    status = models.CharField(max_length=20, choices=STATUS, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.order_id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    colour = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=10, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("product", "user")
