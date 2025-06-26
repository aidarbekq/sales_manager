from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ("id", "created_at")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
        }


class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product", "product_detail", "quantity", "subtotal")
        read_only_fields = ("subtotal",)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer_detail = CustomerSerializer(source="customer", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "customer",
            "customer_detail",
            "status",
            "created_at",
            "discount_percent",
            "tax_percent",
            "shipping_cost",
            "total",
            "items",
        )
        read_only_fields = ("id", "created_at", "total", "shipping_cost")

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        order.recalc_totals()
        order.save(update_fields=["total", "shipping_cost"])
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item in items_data:
                OrderItem.objects.create(order=instance, **item)
        instance.recalc_totals()
        instance.save(update_fields=["total", "shipping_cost"])
        return instance

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("status",)

