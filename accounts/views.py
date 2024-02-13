from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import *


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "api/token",
        "api/token/refresh",
    ]

    return Response(routes)


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
class classUserList(ListAPIView):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ["username", "email"]

# @api_view(["GET"])
# def userList(request):
#     users = User.objects.filter(is_superuser=False)
#     serializer = UserSerializer(users, many=True)
#     filter_backends = [SearchFilter, OrderingFilter]
#     search_fields = ["id"]
#     return Response(serializer.data)


@api_view(["GET"])
def userDetails(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def userUpdate(request, pk):
    try:
        user = User.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(instance=user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

        if "profile_img" in request.FILES:
            user.profile_img = request.FILES["profile_img"]
            user.save()

        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def userDelete(request, pk):
    user = User.objects.get(id=pk)
    user.delete()

    return Response("User deleted")


