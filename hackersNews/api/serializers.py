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
    #is_admin = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        return HNUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.about = validated_data.get('about', instance.about)

        instance.save()
        return instance

    # No muestra email
class UnverifiedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = HNUser
        fields = ['id','username', 'karma','about','date_joined']

# Serializador Siplificado para User (solo muestra su id y username)
class SimplifiedUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = HNUser
        fields = ['id','username']

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    postID = serializers.PrimaryKeyRelatedField(read_only=True, source='post')
    user = SimplifiedUserSerializer(read_only=True, source='user')
    insert_date = serializers.DateTimeField(read_only=True)
    replyTo = serializers.PrimaryKeyRelatedField(read_only=True, source='reply')


    class Meta:
        model = Comment
        fields = ['id','postID','user','insert_date', 'content', 'replyTo']

    
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class SimplifiedPostSerializer(serializers.ModelSerializer):
    author = SimplifiedUserSerializer(read_only=True, source='user')
    commentID = CommentSerializer(read_only=True, source='comment_set')
    class Meta:
        model = Post
        fields = ['id','author','commentID']

class SimplifiedCommentSerializer(serializers.ModelSerializer):
    author = SimplifiedUserSerializer(source ='user', read_only = True)
    post = SimplifiedPostSerializer(source = 'post', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author']

class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    url = serializers.CharField(required=False)
    site = serializers.CharField(required=False, read_only=True)
    text = serializers.CharField(required=False)
    votes = serializers.IntegerField(read_only=True)
    insert_date = serializers.DateTimeField(read_only=True)
    user = HNUserSerializer(read_only=True)
    commentIDs = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source ='comment_set')
    
    class Meta:
        model = Post
        fields = ['id','title', 'url', 'site', 'text', 'votes', 'user', 'insert_date', 'numComments','commentIDs']



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