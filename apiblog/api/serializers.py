from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import requests

from .models import Posts, Likes


class LikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Likes
        fields = '__all__'


class PostsSerializer(serializers.ModelSerializer):
    likes = LikesSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Posts
        fields = '__all__'
        read_only_fields = ['created_by']

    def validate(self, attrs):
        attrs['created_by'] = self.context['request'].user
        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def validate(self, email):
        key = '4a101fae3678cb1cc95498bd128fb474961be089'
        req = {"api_key": key, "email": email}
        check = requests.get("https://api.hunter.io/v2/email-verifier", params=req)
        dat = check.json()
        if dat["errors"][0]["code"] == 400:
            raise serializers.ValidationError('invalid email')
        else:
            return email


    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

