from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer


class LogoutView(DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
