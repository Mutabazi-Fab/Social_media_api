from rest_framework import serializers
from .models import Profile, Post, LikePost, FollowersCount

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = '__all__'

class FollowersCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowersCount
        fields = '__all__'
