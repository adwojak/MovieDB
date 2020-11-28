from typing import Any
from django.contrib.auth.models import User
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, ListModelMixin
from libs.response import SuccessResponse
from libs.mixins import InputCreateModelMixin
from moviesapp.omdbapi import fetch_omdbapi
from moviesapp.serializers import RegisterSerializer
from moviesapp.models import (
    CommentModel,
    MovieModel,
    RatingModel,
)
from moviesapp.serializers import (
    CommentFilterSerializer,
    CommentSerializer,
    MoviesSerializer,
    InputMoviesSerializer,
    RatingsSerializer,
)


class RegisterViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class DeleteUserView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        request.user.delete()
        return SuccessResponse('User deleted', status=HTTP_204_NO_CONTENT)


class RatingsViewSet(ReadOnlyModelViewSet):
    queryset = RatingModel.objects.all()
    serializer_class = RatingsSerializer


class MoviesViewSet(InputCreateModelMixin, ModelViewSet):
    queryset = MovieModel.objects.all()
    serializer_class = MoviesSerializer
    input_serializer_class = InputMoviesSerializer
    # permission_classes = (IsAuthenticated, )

    def create_response(self, data: dict) -> dict:
        return fetch_omdbapi(data['title'])

    def get_serializer(self, *args: Any, **kwargs: Any):
        method = self.request.method
        serializer_instance = super(MoviesViewSet, self).get_serializer(*args, **kwargs)
        if method in ['PUT', 'PATCH']:
            serializer_instance.partial = True
        return serializer_instance

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return SuccessResponse('Movie deleted', status=HTTP_204_NO_CONTENT)


class CommentsViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = super(CommentsViewSet, self).get_queryset()
        request_data = self.request.data
        serializer = CommentFilterSerializer(data=request_data)
        serializer.is_valid()
        movie_id = serializer.validated_data.get('movie_id')
        if movie_id:
            return queryset.filter(movie_id=movie_id)
        return queryset
