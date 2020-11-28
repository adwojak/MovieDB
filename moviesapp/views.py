from datetime import datetime
from django.utils.timezone import now
from django.db.models import Count
from typing import Any
from django.contrib.auth.models import User
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, ListModelMixin
from libs.response import SuccessResponse
from libs.mixins import InputCreateModelMixin
from libs.exceptions import BadDataFormat
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
    TopMoviesSerializer,
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
    permission_classes = (IsAuthenticated,)


class MoviesViewSet(InputCreateModelMixin, ModelViewSet):
    queryset = MovieModel.objects.all()
    serializer_class = MoviesSerializer
    input_serializer_class = InputMoviesSerializer
    permission_classes = (IsAuthenticated, )

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
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(CommentsViewSet, self).get_queryset()
        request_data = self.request.data
        serializer = CommentFilterSerializer(data=request_data)
        serializer.is_valid()
        movie_id = serializer.validated_data.get('movie_id')
        if movie_id:
            return queryset.filter(movie_id=movie_id)
        return queryset


class TopMoviesView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    rank_counter = 0

    def get_element(self, query_object: dict) -> dict:
        self.rank_counter += 1
        return {
            'movie_id': query_object['movie_id'],
            'total_comments': query_object['comments'],
            'rank': self.rank_counter,
        }

    def get(self, request):
        serializer = TopMoviesSerializer(data=request.data)
        if not serializer.is_valid():
            raise BadDataFormat(serializer.errors)
        date_from = serializer.validated_data.get('date_from', datetime.min)
        date_to = serializer.validated_data.get('date_to', now())
        queryset = CommentModel.objects.filter(post_date__gte=date_from, post_date__lte=date_to)
        counted_queryset = queryset.values('movie_id').annotate(comments=Count('movie_id'))
        return SuccessResponse([self.get_element(element) for element in counted_queryset])
