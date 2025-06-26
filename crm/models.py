from django.db import models
from django.utils import timezone

class Customer(models.Model):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(default=timezone.now)
    discount_percent = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    tax_percent = models.DecimalField(max_digits=4, decimal_places=2, default=12)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def recalc_totals(self):
        positions_total = sum(item.subtotal for item in self.items.all())

        # глобальная акция: -10%
        global_disc = 0.1 if positions_total > 150_000 else 0

        discount_total = positions_total * (self.discount_percent + global_disc) / 100
        tax_total = (positions_total - discount_total) * self.tax_percent / 100

        # бесплатная доставка при заказе > 2000
        if positions_total - discount_total > 2_000:
            self.shipping_cost = 0

        self.total = positions_total - discount_total + tax_total + self.shipping_cost

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} ({self.customer})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.order.status == "confirmed":
            self.product.stock_quantity = models.F("stock_quantity") - self.quantity
            self.product.save(update_fields=["stock_quantity"])

    class Meta:
        unique_together = ("order", "product")
