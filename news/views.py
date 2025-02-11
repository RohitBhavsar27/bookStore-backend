from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from news.models import News  # MongoEngine model
from news.serializers import NewsSerializer  # Custom serializer

# Create your views here.


# ? GET ALL BOOKS
@api_view(["GET"])
def getNewsData(request):
    try:
        # Retrieve all books
        allNews = News.objects()

        # Serialize the data
        serializer = NewsSerializer(allNews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
