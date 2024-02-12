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
from django.shortcuts import get_object_or_404

from .models import Room
from .serializers import *
from rest_framework.response import Response
from apps.likes.models import Like
from apps.account.permissions import IsActive
from apps.comments.serializers import CommentSerializer
from apps.comments.models import Comment


User = get_user_model()


class Pagination(PageNumberPagination):
    page_size = 8
    page_query_param = 'page'


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title', )
    filterset_fields = ('count_rooms',)

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

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def comments(self, request, pk, comment_id=None):
        if request.method == 'GET':
            post = self.get_object()
            comment = post.comments.all()
            serializer = CommentSerializer(
                instance=comment,
                many=True
            )
            return Response(serializer.data, status=200)

        elif request.method == 'POST':
            post = self.get_object()
            user = request.user
            body = request.data.get('body')
            if not body:
                return Response('Message is empty', status=400)
            serializer = CommentSerializer(
                data={
                    'post': post.id,
                    'body': body
                }
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user)
            return Response(serializer.data, status=201)

        elif request.method == 'DELETE':
            comment_id = request.query_params.get('comment_id')
            if comment_id:
                comment = get_object_or_404(
                    Comment,
                    id=comment_id,
                    post__id=pk
                )
                comment.delete()
                return Response('Comment successfully deleted', status=204)
            return Response('Invalid comment_id', status=404)


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




