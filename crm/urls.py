from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CustomerViewSet, ProductViewSet, OrderViewSet, ReportViewSet

router = DefaultRouter()
router.register("customers", CustomerViewSet)
router.register("products", ProductViewSet)
router.register("orders", OrderViewSet, basename="orders")
router.register("reports/sales", ReportViewSet, basename="reports-sales")

urlpatterns = [
    path("", include(router.urls)),
]
