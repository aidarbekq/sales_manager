from datetime import datetime
from decimal import Decimal
from django.db.models import Sum, Count
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from .models import Order, Product, Customer

def generate_sales_report_pdf(start_date: str, end_date: str) -> bytes:
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    orders = (
        Order.objects.filter(created_at__date__gte=start, created_at__date__lte=end)
        .select_related("customer")
        .prefetch_related("items__product")
    )

    revenue = orders.aggregate(total=Sum("total"))["total"] or Decimal("0")
    top_customers = (
        Customer.objects.filter(orders__in=orders)
        .annotate(total=Sum("orders__total"))
        .order_by("-total")[:5]
    )
    popular_product = (
        Product.objects.filter(orderitem__order__in=orders)
        .annotate(qty=Sum("orderitem__quantity"))
        .order_by("-qty")
        .first()
    )

    context = {
        "start": start_date,
        "end": end_date,
        "revenue": revenue,
        "orders_count": orders.count(),
        "top_customers": top_customers,
        "popular_product": popular_product,
        "orders": orders,
    }

    html = render_to_string("reports/sales_report.html", context)
    pdf = BytesIO()
    HTML(string=html, base_url="").write_pdf(pdf)
    return pdf.getvalue()
