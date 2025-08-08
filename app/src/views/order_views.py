from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request


from src.serializers.order_serializers import OrderSerializer, BookingSerializer
from src.services.order_services import OrderCreateSrv, FreeBookingSrv


class OrderCreateView(APIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """POST handler for creating order and booking"""
        self.request: Request
        serializer = OrderSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, dict):
            print(serializer)
            order_create_srv = OrderCreateSrv(
                serializer_validate_data=serializer.validated_data,
                serialzier_data=serializer.data,
            )
            return order_create_srv.execute()
        return Response(
            {
                "message": "Bad error",
                "success": False,
                "data": [],
            },
            status=422,
        )


class FreeBookingView(APIView):
    serializer_class = BookingSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """POST handler for creating order and booking"""
        self.request: Request
        serializer = BookingSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, dict):
            free_booking_src = FreeBookingSrv(
                serializer_validated_data=serializer.validated_data,
            )
            return free_booking_src.execute()

        return Response(
            {
                "message": "Bad error",
                "success": False,
                "data": [],
            },
            status=422,
        )
