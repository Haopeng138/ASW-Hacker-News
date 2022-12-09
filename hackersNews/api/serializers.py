from rest_framework import serializers
from accounts.models import HNUser
from homepage.models import *

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """ Model Serializer with Dynamic Set of Fields 
        ref : https://stackoverflow.com/questions/23643204/django-rest-framework-dynamically-return-subset-of-fields"""

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if fields:
            print("Apllying fields")
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            print(allowed)
            existing = set(self.fields.keys())
            print(existing)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class HNUserSerializer(DynamicFieldsModelSerializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(required=False, allow_blank=False, max_length=255)
    email = serializers.EmailField(read_only=True)
    karma = serializers.IntegerField(read_only=True)

    date_joined = serializers.DateField(read_only=True)
    about = serializers.CharField(allow_blank=True, required=False)
    #is_admin = serializers.BooleanField(read_only=True)

    class Meta:
        model = HNUser
        fields = ['id','username','email','karma', 'date_joined', 'about']

    def create(**validated_data):
        return HNUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.about = validated_data.get('about', instance.about)

        instance.save()
        return instance

class CommentSerializer(DynamicFieldsModelSerializer):
    id = serializers.IntegerField(read_only=True)
    postID = serializers.PrimaryKeyRelatedField(read_only=True, source='post')
    user = HNUserSerializer(read_only=True, source='user', fields=('id','username'))
    insert_date = serializers.DateTimeField(read_only=True)
    replyTo = serializers.PrimaryKeyRelatedField(read_only=True, source='reply')


    class Meta:
        model = Comment
        fields = ['id','postID','user','insert_date', 'content', 'replyTo']

    
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class SimplifiedPostSerializer(serializers.ModelSerializer):
    author = HNUserSerializer(read_only=True, source='user')
    commentID = CommentSerializer(read_only=True, source='comment_set')
    class Meta:
        model = Post
        fields = ['id','author','commentID']

class SimplifiedCommentSerializer(serializers.ModelSerializer):
    author = HNUserSerializer(source ='user', read_only = True)
    post = SimplifiedPostSerializer(source = 'post', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author']

class PostSerializer(DynamicFieldsModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    title = serializers.CharField(required=True)
    url = serializers.CharField(required=False)
    site = serializers.CharField(required=False, read_only=True)
    text = serializers.CharField(required=False)
    
    # votes = serializers.IntegerField(read_only=True)
    votes = serializers.IntegerField()
    insert_date = serializers.DateTimeField(read_only=True)
    
    user = HNUserSerializer(read_only=True)
    #userID = serializers.PrimaryKeyRelatedField(write_only=True, queryset='id')

    numComments = serializers.IntegerField(read_only=True)
    commentIDs = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source ='comment_set')
    
    class Meta:
        model = Post
        fields = ['id','title', 'url', 'site', 'text', 'votes', 'user', 'insert_date', 'numComments','commentIDs']


# Deprecado/Inutil
class PostVoteSerializer(serializers.ModelSerializer):
    user = HNUserSerializer()
    post = PostSerializer()

    class Meta:
        model = PostVoteTracking
        fields = ['user', 'post']

# Deprecado/Inutil
class CommentVoteSerializer(serializers.ModelSerializer):
    user = HNUserSerializer()
    commet = CommentSerializer()

    class Meta:
        model = CommentVoteTracking
        fields = ['user', 'comment']