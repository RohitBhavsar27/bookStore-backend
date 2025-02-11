from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from orders.models import Orders, Address, Books
from orders.serializers import OrdersSerializer


@api_view(["POST"])
def newOrder(request):
    try:
        # Parse and validate data using the serializer
        serializer = OrdersSerializer(data=request.data)
        if serializer.is_valid():
            # Extract validated data
            validated_data = serializer.validated_data

            # Create Address object
            address_data = validated_data.pop("address")
            address = Address(**address_data)

            # Fetch Book references from productIds
            product_ids = validated_data.pop("productIds")
            books = Books.objects(id__in=product_ids)
            if len(books) != len(product_ids):
                return Response(
                    {"error": "Invalid productIds provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create and save the Checkout document
            checkout = Orders(address=address, productIds=list(books), **validated_data)
            checkout.save()

            return Response(
                {
                    "message": "Checkout created successfully!",
                    "orderId": str(checkout.id),
                    "success": True,
                },
                status=status.HTTP_201_CREATED,
            )

        # Handle validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def getOrder(request, email):
    orders = Orders.objects(email=email)  # Fetch orders based on email

    if not orders:
        # ✅ Instead of a 404 error, return an empty list with a success status
        return Response(
            {"orders": [], "message": f"No orders found for {email}."},
            status=status.HTTP_200_OK,
        )

    serializer = OrdersSerializer(orders, many=True)  # Serialize multiple orders
    return Response({"orders": serializer.data}, status=status.HTTP_200_OK)
