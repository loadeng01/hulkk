from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework.views import APIView

from .models import Room
from .serializers import *
from rest_framework.response import Response
from apps.likes.models import Like
from apps.account.permissions import IsActive


User = get_user_model()


class Pagination(PageNumberPagination):
    page_size = 8
    page_query_param = 'page'


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title', )
    filterset_fields = ('category',)

    def get_serializer_class(self):
        if self.action == 'list':
            return RoomListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return RoomCreateSerializer
        return RoomDetailSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE', 'POST'):
            return IsAdminUser(),
        return AllowAny(),

    @action(['POST'], detail=True)
    def likes(self, request, pk, like_id=None):
        post = self.get_object()
        user = request.user
        like, is_created = Like.objects.get_or_create(post=post, owner=user)

        if is_created:
            return Response('Liked', status=200)
        like.is_liked = not like.is_liked
        like.save()

        if like.is_liked:
            return Response('Liked', status=200)
        return Response('Unliked', status=200)


class UserFavoritesListView(APIView):
    permission_classes = IsActive,

    def get(self, request):
        user = request.user
        likes = Like.objects.filter(owner=user)
        data = []

        for item in likes:
            print(item, '11111111111111')
            serializer = RoomSerializer(item.post)
            data.append(serializer.data)

        return Response(data, status=200)




