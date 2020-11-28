from django.db.models import (
    CharField,
    IntegerField,
    ManyToManyField,
    Model,
)


class RatingModel(Model):
    source = CharField(max_length=50)
    value = CharField(max_length=10)

    def __repr__(self):
        return self.__class__.__name__


class MovieModel(Model):
    title = CharField(max_length=200)
    year = CharField(max_length=20, blank=True)
    rated = CharField(max_length=10, blank=True)
    released = CharField(max_length=20, blank=True)
    runtime = CharField(max_length=10, blank=True)
    genre = CharField(max_length=500, blank=True)
    director = CharField(max_length=500, blank=True)
    writer = CharField(max_length=500, blank=True)
    actors = CharField(max_length=500, blank=True)
    plot = CharField(max_length=800, blank=True)
    language = CharField(max_length=50, blank=True)
    country = CharField(max_length=200, blank=True)
    awards = CharField(max_length=200, blank=True)
    poster = CharField(max_length=300, blank=True)
    ratings = ManyToManyField(RatingModel, blank=True)
    metascore = CharField(max_length=10, blank=True)
    imdb_rating = CharField(max_length=10, blank=True)
    imdb_votes = CharField(max_length=20)
    imdb_id = CharField(max_length=15, blank=True)
    type = CharField(max_length=60, blank=True)
    total_seasons = CharField(max_length=20, blank=True)
    dvd = CharField(max_length=20, blank=True)
    production = CharField(max_length=300, blank=True)
    website = CharField(max_length=300, blank=True)

    def __repr__(self):
        return self.__class__.__name__
