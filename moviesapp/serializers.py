from django.contrib.auth.models import User
from rest_framework.serializers import (
    CharField,
    DateTimeField,
    IntegerField,
    Serializer,
    HyperlinkedModelSerializer,
)
from moviesapp.models import (
    CommentModel,
    RatingModel,
    MovieModel,
)
from libs.exceptions import MovieDoesNotExist
from libs.errors import MOVIE_DOES_NOT_EXIST


class RegisterSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        instance = User(**validated_data)
        instance.set_password(raw_password)
        instance.save()
        return instance


class RatingsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = RatingModel
        fields = '__all__'

    def create(self, validated_data):
        try:
            return self.Meta.model.objects.get_or_create(**validated_data)[0]
        except self.Meta.model.MultipleObjectsReturned:
            return self.Meta.model.objects.filter(**validated_data).first()


class MoviesSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = MovieModel
        fields = '__all__'

    ratings = RatingsSerializer(many=True)

    def create(self, validated_data):
        ratings = validated_data.pop('ratings')
        try:
            return self.Meta.model.objects.get(**validated_data)
        except self.Meta.model.DoesNotExist:
            ratings_models = RatingsSerializer(many=True).create(ratings)
            instance = self.Meta.model.objects.create(**validated_data)
            instance.ratings.set(ratings_models)
            return instance
        except self.Meta.model.MultipleObjectsReturned:
            return self.Meta.model.objects.filter(**validated_data).first()

    def update(self, instance, validated_data):
        ratings = validated_data.pop('ratings', None)
        [setattr(instance, attr, value) for attr, value in validated_data.items()]
        if ratings:
            ratings_models = RatingsSerializer(many=True, partial=True).create(ratings)
            instance.ratings.set(ratings_models)
        instance.save()
        return instance


class InputMoviesSerializer(Serializer):
    title = CharField(max_length=100)


class CommentFilterSerializer(Serializer):
    movie_id = IntegerField(required=False)


class CommentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['movie_id', 'comment']

    def create(self, validated_data):
        movie_id = validated_data['movie_id']
        try:
            MovieModel.objects.get(id=movie_id)
        except MovieModel.DoesNotExist:
            raise MovieDoesNotExist(MOVIE_DOES_NOT_EXIST.format(movie_id))
        return self.Meta.model.objects.create(**validated_data)


class TopMoviesSerializer(Serializer):
    date_from = DateTimeField(required=False)
    date_to = DateTimeField(required=False)
