from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Profile, FollowersCount
from .serializers import PostSerializer, ProfileSerializer, FollowersCountSerializer
from django.shortcuts import get_object_or_404

# List all posts or create a new post
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Like or unlike a post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    # Assume we have a boolean field 'liked' on the post model and a 'toggle_like' method
    post.toggle_like(request.user)
    return Response({"message": f"Post {'liked' if post.liked else 'unliked'} successfully!"}, status=status.HTTP_200_OK)

# Retrieve a user's profile by username
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_detail(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Follow or unfollow a user
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, username):
    try:
        profile_to_follow = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    follower = FollowersCount.objects.filter(user=profile_to_follow.user, follower=request.user)

    if follower.exists():
        follower.delete()
        message = "Unfollowed successfully."
    else:
        FollowersCount.objects.create(user=profile_to_follow.user, follower=request.user)
        message = "Followed successfully."

    return Response({"message": message}, status=status.HTTP_200_OK)

# Get the list of followers for a user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def followers_list(request, username):
    followers = FollowersCount.objects.filter(user__username=username)
    if not followers.exists():
        return Response({"message": "This user has no followers."}, status=status.HTTP_404_NOT_FOUND)

    serializer = FollowersCountSerializer(followers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Get the list of users that a specific user is following
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def following_list(request, username):
    following = FollowersCount.objects.filter(follower__username=username)
    if not following.exists():
        return Response({"message": "This user is not following anyone."}, status=status.HTTP_404_NOT_FOUND)

    serializer = FollowersCountSerializer(following, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
