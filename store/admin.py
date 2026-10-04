from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Brand,
    Category,
    Colour,
    Order,
    OrderItem,
    Product,
    ProductColourImage,
    Review,
    Size,
)


admin.site.site_header = "CASUAL · Store management"
admin.site.site_title = "Casual admin"
admin.site.index_title = "Store overview"


class ProductColourImageInline(admin.TabularInline):
    model = ProductColourImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "category",
        "selling_price_display",
        "discount_percent",
        "stock_status",
        "active",
    )
    list_filter = ("category", "brand", "active", "colours")
    search_fields = ("name", "brand__name", "category__name", "description")
    list_select_related = ("brand", "category")
    list_editable = ("active",)
    list_per_page = 25
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    filter_horizontal = ("colours", "sizes")
    inlines = (ProductColourImageInline,)

    @admin.display(description="Selling price", ordering="original_price")
    def selling_price_display(self, obj):
        return f"₹{obj.selling_price:,.2f}"

    @admin.display(description="Inventory", ordering="stock")
    def stock_status(self, obj):
        if obj.stock == 0:
            label, css_class = "Out of stock", "admin-stock-empty"
        elif obj.stock <= 5:
            label, css_class = f"Low · {obj.stock}", "admin-stock-low"
        else:
            label, css_class = f"In stock · {obj.stock}", "admin-stock-ok"
        return format_html('<span class="{}">{}</span>', css_class, label)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ("product",)
    readonly_fields = ("product", "colour", "size", "quantity", "price")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "full_name",
        "status",
        "payment_method",
        "payment_status",
        "total_amount",
        "created_at",
    )
    list_filter = ("status", "payment_method", "payment_status", "created_at")
    search_fields = ("order_id", "full_name", "email", "mobile", "user__username")
    list_select_related = ("user",)
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    inlines = (OrderItemInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Colour)
class ColourAdmin(admin.ModelAdmin):
    list_display = ("name", "colour_swatch", "hex_code")
    search_fields = ("name", "hex_code")
    ordering = ("name",)

    @admin.display(description="Preview")
    def colour_swatch(self, obj):
        return format_html(
            '<span class="admin-colour-swatch" style="--swatch: {}"></span>',
            obj.hex_code,
        )


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(ProductColourImage)
class ProductColourImageAdmin(admin.ModelAdmin):
    list_display = ("product", "colour")
    list_select_related = ("product", "colour")
    list_filter = ("colour",)
    search_fields = ("product__name", "colour__name")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "colour", "size", "quantity", "price")
    list_select_related = ("order", "product")
    search_fields = ("order__order_id", "product__name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    list_select_related = ("product", "user")
    search_fields = ("product__name", "user__username", "comment")
    readonly_fields = ("created_at",)
