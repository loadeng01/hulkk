from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny

from .models import Room
from .serializers import *


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







