from .models import Book
from .serializers import BookSerializer
from rest_framework.viewsets import ModelViewSet
# Create your views here.

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer