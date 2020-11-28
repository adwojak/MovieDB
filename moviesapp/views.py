from django.contrib.auth.models import User
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin
from libs.response import SuccessResponse
from moviesapp.serializers import RegisterSerializer

from rest_framework.response import Response
from moviesapp.omdbapi import fetch_omdbapi


class RegisterViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class DeleteUserView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        request.user.delete()
        return Response(fetch_omdbapi('Matrix'))
        # return SuccessResponse('User deleted', status=HTTP_204_NO_CONTENT)
