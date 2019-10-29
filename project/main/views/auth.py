from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from ..serializers import users_serializer


class CheckTokenView(APIView):
    def get(self, request):
        current_token = request.query_params.get('token', None)

        if not current_token:
            return Response(data={'message': 'Missing token'}, status=status.HTTP_400_BAD_REQUEST)

        get_object_or_404(Token, key=current_token)
        return Response({"valid": True})


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(
            request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        serialized_user = users_serializer.UserSerializerAll(token.user)
        return Response({'token': token.key, 'id': token.user_id,
                         'username': serialized_user.data['username'],
                         'groups': serialized_user.data['groups']})
