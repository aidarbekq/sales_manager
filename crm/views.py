from django.http import HttpResponse
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, Product, Order
from .serializers import (
    CustomerSerializer,
    ProductSerializer,
    OrderSerializer, OrderStatusSerializer,
)
from .permissions import StaffOrReadOnly
from .services import generate_sales_report_pdf

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [StaffOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company_name"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [StaffOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_active"]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product").select_related("customer")
    serializer_class = OrderSerializer
    permission_classes = [StaffOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "created_at", "customer__company_name"]

    @extend_schema(
        methods=["PATCH"],
        request=OrderStatusSerializer,
        responses={200: OrderSerializer},
        description="Меняет ТОЛЬКО поле `status` заказа"
    )
    @action(detail=True, methods=["patch"])
    def status(self, request, pk=None):
        order = self.get_object()
        serializer = OrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order.status = serializer.validated_data["status"]
        order.save(update_fields=["status"])
        return Response(OrderSerializer(order, context=self.get_serializer_context()).data)


class ReportViewSet(viewsets.ViewSet):
    permission_classes = [StaffOrReadOnly]

    @extend_schema(
        summary="Скачать отчёт о продажах",
        description="Генерирует PDF за период."
                    "НЕ ПЕРЕПУТАЙТЕ START и END!",
        parameters=[
            OpenApiParameter("start", OpenApiTypes.DATE, OpenApiParameter.QUERY, required=True),
            OpenApiParameter("end", OpenApiTypes.DATE, OpenApiParameter.QUERY, required=True),
        ],
        responses={
            200: OpenApiResponse(
                description="PDF-файл с отчётом",
                response=OpenApiTypes.BINARY,
            ),
            400: OpenApiResponse(description="start and end required"),
        },
    )
    def list(self, request):
        start = request.query_params.get("start")
        end = request.query_params.get("end")
        if not (start and end):
            return Response({"detail": "start and end required"}, status=400)

        pdf_bytes = generate_sales_report_pdf(start, end)

        return HttpResponse(
            pdf_bytes,
            content_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="sales_{start}_{end}.pdf"'
            },
        )
