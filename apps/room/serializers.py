from rest_framework import serializers
from .models import *


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImages
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Room
        fields = ('title', 'body', 'category', 'preview', 'images')

    def create(self, validated_data):
        request = self.context.get('request')
        post = Room.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        for image in images_data:
            RoomImages.objects.create(image=image, post=post)
        return post