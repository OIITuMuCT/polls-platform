from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render



from store.models import Book
from store.serializers import BookSerializer


# Create your views here.

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_fields = ['price']
    search_fields = ['title','price', 'author',]

def auth(request):
    return render(request, 'oauth.html')
