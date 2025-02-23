from bson import ObjectId
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from books.models import Books  # MongoEngine model
from books.serializers import BookSerializer  # Custom serializer
from middleware.jwt_middleware import verify_admin_token


# ? ADD A NEW BOOK
@api_view(["POST"])
@verify_admin_token
def addBook(request):
    try:
        book_data = request.data

        # Check if a book with the same title already exists
        if Books.objects(title=book_data.get("title")).count() > 0:
            return Response(
                {"error": "A book with this title already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate input data using the serializer
        serializer = BookSerializer(data=book_data)
        if serializer.is_valid():
            # Save the validated data to the database
            book = Books(**serializer.validated_data)
            book.save()

            # Serialize the newly created book
            serialized_book = BookSerializer(book)
            return Response(
                {
                    "book": serialized_book.data,
                    "success": True,
                    "message": "Book added successfully",
                },
                status=status.HTTP_201_CREATED,
            )

        # Handle validation errors
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ? GET ALL BOOKS
@api_view(["GET"])
def getAllBooks(request):
    try:
        # Retrieve all books, ordered by creation date (latest first)
        allBooks = Books.objects.order_by("-created_at")

        # Serialize the data
        serializer = BookSerializer(allBooks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ? GET A SINGLE BOOK
@api_view(["GET"])
def getBook(request, book_id):
    try:
        # Validate the ObjectId (optional)
        if not ObjectId.is_valid(book_id):
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Retrieve the book by ID
        book = Books.objects.get(id=book_id)  # Use `get` to fetch the document

        # Serialize the book
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Books.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ? UPDATE AN EXISTING BOOK
@api_view(["PUT"])
@verify_admin_token
def updateBook(request, book_id):
    try:
        # Check if the ObjectId is valid
        if not ObjectId.is_valid(book_id):
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the book exists
        book = Books.objects.get(id=book_id)

        # Validate the input data
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            # Update the existing book's fields
            for field, value in serializer.validated_data.items():
                setattr(book, field, value)
            book.save()  # Save the updated document

            # Serialize the updated book
            updated_serializer = BookSerializer(book)
            return Response(
                {
                    "book": updated_serializer.data,
                    "success": True,
                    "message": "Book updated successfully",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
    except Books.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ! DELETE AN EXISTING BOOK
@api_view(["DELETE"])
@verify_admin_token
def deleteBook(request, book_id):
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(book_id):
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Get and delete the book
        book = Books.objects.get(id=book_id)
        book.delete()  # Delete the document
        return Response(
            {"success": True, "message": "Book deleted successfully"},
            status=status.HTTP_200_OK,
        )

    except Books.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


