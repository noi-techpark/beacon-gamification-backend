from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from main.serializers import users_serializer

from ..utils.permissions import CustomDjangoModelPermissions, IsGamersUser


class UserDetailsView(RetrieveAPIView):
    permission_classes = (CustomDjangoModelPermissions,)
    queryset = User.objects.all()

    serializer_class = users_serializer.UserSerializer


class UserListView(ListAPIView):
    permission_classes = (CustomDjangoModelPermissions,)
    queryset = User.objects.all()

    serializer_class = users_serializer.UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = (CustomDjangoModelPermissions,)

    queryset = User.objects.all()
    serializer_class = users_serializer.UserSerializerCreate


class AddUserToGroupView(APIView):
    permission_classes = (CustomDjangoModelPermissions,)
    queryset = User.objects.all()

    def post(self, request, pkGroup, pkUser):
        user = User.objects.get(id=pkUser)
        group = Group.objects.get(id=pkGroup)
        user.groups.add(group)

        return Response({"Message": "User added to the group"})


class AddPoints(APIView):
    permission_classes = (IsGamersUser,)

    def post(self, request, format=None):
        pk_user = request.data.get('pk_user', None)
        points = request.data.get('points', None)
        if not pk_user:
            return Response("Missing parameter pk_user", status.HTTP_400_BAD_REQUEST)
        if not points:
            return Response("Missing parameter points", status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=pk_user)
        if user.extendeduser.points:
            user.extendeduser.points = user.extendeduser.points + points
        else:
            user.extendeduser.points = points
        user.extendeduser.save()

        return Response({"points": user.extendeduser.points})
