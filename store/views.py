from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from store.permissions import IsOwnerOrStaffOrReadOnly
from store.models import Book, UserBookRelation
from store.serializers import BookSerializer, UserBookRelationSerializer


# Create your views here.

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_fields = ['price']
    search_fields = ['title', 'price', 'author',]

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

class UserBooksRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj , created = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                         book_id=self.kwargs['book'])
        print('created', created)
        return obj

def auth(request):
    return render(request, 'oauth.html')
