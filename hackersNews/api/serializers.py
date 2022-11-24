from rest_framework import serializers
from accounts.models import HNUser


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
