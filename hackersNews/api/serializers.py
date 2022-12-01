from rest_framework import serializers
from accounts.models import HNUser
from homepage.models import *


class HNUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False, allow_blank=False, max_length=255)
    email = serializers.EmailField(read_only=True)
    karma = serializers.IntegerField(read_only=True)
    date_joined = serializers.DateField(read_only=True)
    about = serializers.CharField(allow_blank=True, required=False)
    is_admin = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        return HNUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.about = validated_data.get('about', instance.about)

        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    insert_date = serializers.DateTimeField(read_only=True)
    user = HNUserSerializer(read_only=True)
    #post = PostSerializer()

    class Meta:
        model = Comment
        fields = ['insert_date', 'content', 'user']


class PostSerializer(serializers.ModelSerializer):
    url = serializers.CharField(required=False)
    site = serializers.CharField(required=False, read_only=True)
    votes = serializers.IntegerField(read_only=True)
    insert_date = serializers.DateTimeField(read_only=True)
    user = HNUserSerializer(read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'url', 'site', 'votes', 'user', 'insert_date', 'comment_set']


class PostVoteSerializer(serializers.ModelSerializer):
    user = HNUserSerializer()
    post = PostSerializer()

    class Meta:
        model = PostVoteTracking
        fields = ['user', 'post']


class CommentVoteSerializer(serializers.ModelSerializer):
    user = HNUserSerializer()
    commet = CommentSerializer()

    class Meta:
        model = CommentVoteTracking
        fields = ['user', 'comment']