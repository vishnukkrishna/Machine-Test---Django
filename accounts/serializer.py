from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


# to get the totken
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["is_admin"] = user.is_superuser

        return token
    
class UserSerializer(serializers.ModelSerializer):
    # Model is passed to serializer
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "profile_img"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

