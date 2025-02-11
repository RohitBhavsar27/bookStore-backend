from rest_framework import serializers
from orders.models import Orders, Address, Books


class AddressSerializer(serializers.Serializer):
    street = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    zipcode = serializers.CharField(max_length=20)


class OrdersSerializer(serializers.Serializer):
    id = serializers.CharField(source="pk", read_only=True)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=255)
    phone = serializers.CharField(max_length=20)
    address = AddressSerializer()
    totalPrice = serializers.FloatField()
    created_at = serializers.DateTimeField(read_only=True)
    # productIds = (
    #     serializers.SerializerMethodField()
    # )  # Override productIds to return only IDs

    productIds = serializers.ListField(
        child=serializers.CharField(),  # Product IDs as strings
        required=True,  # Ensure the field is present
    )

    class Meta:
        model = Orders
        fields = ["id", "name", "email", "phone", "address", "productIds", "totalPrice"]


    def to_representation(self, instance):
        """
        Override this method to send only product IDs to the frontend.
        """
        representation = super().to_representation(instance)
        # Convert product objects into a list of IDs for frontend response
        representation["productIds"] = [str(book.id) for book in instance.productIds]
        return representation
