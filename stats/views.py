from django.http import JsonResponse
from orders.models import Orders
from books.models import Books
from mongoengine.queryset.visitor import Q
from datetime import datetime
from mongoengine import connection
from rest_framework.decorators import api_view
from middleware.jwt_middleware import verify_admin_token


@api_view(["GET"])
@verify_admin_token
def admin_stats(request):
    try:
        # Get the database connection
        db = connection.get_db()

        # 1. Total number of orders
        total_orders = Orders.objects.count()

        # 2. Total sales (sum of all totalPrice from orders)
        total_sales = list(
            db.orders.aggregate(
                [
                    {
                        "$group": {
                            "_id": None,
                            "totalSales": {"$sum": "$totalPrice"},
                        }
                    }
                ]
            )
        )
        total_sales = total_sales[0]["totalSales"] if total_sales else 0

        # 3. Trending books statistics
        trending_books_count = list(
            db.books.aggregate(
                [
                    {"$match": {"trending": True}},
                    {"$count": "trendingBooksCount"},
                ]
            )
        )
        trending_books = (
            trending_books_count[0]["trendingBooksCount"] if trending_books_count else 0
        )

        # 4. Total number of books
        total_books = Books.objects.count()

        # 5. Monthly sales (group by month and sum total sales for each month)
        monthly_sales = list(
            db.orders.aggregate(
                [
                    {
                        "$group": {
                            "_id": {
                                "$dateToString": {
                                    "format": "%Y-%m",
                                    "date": "$created_at",
                                }
                            },
                            "totalSales": {"$sum": "$totalPrice"},
                            "totalOrders": {"$sum": 1},
                        }
                    },
                    {"$sort": {"_id": 1}},  # Sort by month
                ]
            )
        )

        # Prepare the response
        response_data = {
            "totalOrders": total_orders,
            "totalSales": total_sales,
            "trendingBooks": trending_books,
            "totalBooks": total_books,
            "monthlySales": monthly_sales,
        }

        return JsonResponse(response_data, status=200)

    except Exception as e:
        print("Error fetching admin stats:", e)
        return JsonResponse({"message": "Failed to fetch admin stats"}, status=500)
