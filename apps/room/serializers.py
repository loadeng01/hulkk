from rest_framework import serializers
from .models import *
from apps.category.models import Category


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImages
        fields = '__all__'


class RoomCreateSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())
    images = RoomImageSerializer(many=True, required=False)

    class Meta:
        model = Room
        # fields = ('number', 'count_rooms', 'state', 'category', 'preview', 'images')
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        post = Room.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')

        if images_data:
            for image in images_data:
                RoomImages.objects.create(image=image, post=post)

        return post


class RoomListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('id', 'number', 'count_rooms', 'state', 'preview')


class RoomDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    images = RoomImageSerializer(many=True)

    class Meta:
        model = Room
        fields = '__all__'
