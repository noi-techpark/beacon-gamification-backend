from django.contrib.auth.models import User, Group
from rest_framework import serializers

from ..models import ExtendedUser


class ExtendedUserSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user.id')

    class Meta:
        model = ExtendedUser
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    points = serializers.IntegerField(source='extendeduser.points')

    class Meta:
        model = User
        fields = ('username', 'points')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializerAll(serializers.ModelSerializer):
    points = serializers.IntegerField(source='extendeduser.points')
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'


class UserSerializerCreate(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        password = validated_data['password']
        password2 = validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Password must match'})
        user.set_password(password)
        user.save()
        return user
