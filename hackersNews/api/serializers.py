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
            #print("Apllying fields")
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            #print(allowed)
            existing = set(self.fields.keys())
            #print(existing)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


### ---     USER SERIALIZER     --- ###
class HNUserSerializer(DynamicFieldsModelSerializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(required=False, allow_blank=False, max_length=255)
    email = serializers.EmailField(required=True)
    karma = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    date_joined = serializers.DateField(read_only=True)
    about = serializers.CharField(allow_blank=True, required=False)
    #is_admin = serializers.BooleanField(read_only=True)

    class Meta:
        model = HNUser
        fields = ['id','username','email','karma', 'password', 'date_joined', 'about']
    
    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        pw = validated_data.get('password')

        return HNUser.objects.create_user(username=username,email=email,password=pw)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.about = validated_data.get('about', instance.about)

        instance.save()
        return instance

class UpdateUserSerializer(HNUserSerializer):
    email = serializers.EmailField(required=False)
    class Meta:
        model = HNUser
        fields = ['id','username','email','karma', 'date_joined', 'about']

### ---   COMMENTS SERIALIZER   --- ###
class CommentSerializer(DynamicFieldsModelSerializer):
    id = serializers.IntegerField(read_only=True)

    postID = serializers.PrimaryKeyRelatedField(read_only=True, source='post')
    user = HNUserSerializer(read_only=True, fields=('id','username'))

    insert_date = serializers.DateTimeField(read_only=True)
    content = serializers.CharField(allow_blank=False, required=True)

    replyTo = serializers.PrimaryKeyRelatedField(read_only=True, source='reply')

    class Meta:
        model = Comment
        fields = ['id','postID','user','insert_date', 'content', 'replyTo']
    
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

### ---     POST SERIALIZER     --- ###
class PostSerializer(DynamicFieldsModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    title = serializers.CharField(required=True, allow_blank=False)
    url = serializers.CharField(required=False, allow_blank=True)
    site = serializers.CharField(read_only=True)
    text = serializers.CharField(required=False, allow_blank=True)
    
    votes = serializers.IntegerField(read_only=True)
    insert_date = serializers.DateTimeField(read_only=True)
    
    user = HNUserSerializer(read_only=True, fields=('username','id','karma'))

    numComments = serializers.IntegerField(read_only=True)
    commentIDs = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source ='comment_set')
    
    class Meta:
        model = Post
        fields = ['id','title', 'url', 'site', 'text', 'votes', 'user', 'insert_date', 'numComments','commentIDs']
