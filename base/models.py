from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models import Count
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=250)

class Movies(models.Model):

    '''
        The complete list of movies.
    '''

    uuid = models.UUIDField()
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='genres', blank=True)

class Collection(models.Model):

    '''
        Mapping of movies to user 
    '''

    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movies, related_name='movies', blank=True)


class General(models.Model):
    request_count = models.IntegerField(default=0)