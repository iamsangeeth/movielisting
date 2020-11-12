from rest_framework import serializers
from base.models import *
from rest_framework.authtoken.models import Token

class MovieSerializer(serializers.ModelSerializer):
    '''
        Serializing movies database
    '''
    genres = serializers.CharField(allow_null=True, allow_blank=True)
    class Meta:
        model = Movies
        exclude = ('id', )

    def to_representation(self, instance):
        '''
            Returns changed 'genre' field to call get_genres
        '''
        self.fields['genres'] =  serializers.SerializerMethodField()
        return super(MovieSerializer, self).to_representation(instance)

    def get_genres(self, obj):
        '''
            Showing genres to front comma seperated
        '''
        return ",".join(obj.genres.all().values_list('name', flat=True))


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name = validated_data['username'],
            email = validated_data['username'].lower(),
            username = validated_data['username'].lower(),
            password = validated_data['password'],
        )
        return user

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)
    class Meta:
        model = Collection
        exclude = ('user',)

    def create(self, validated_data):
        movies = []
        if validated_data.get('movies', None):
            movies = validated_data.pop('movies')
        collection_obj = Collection.objects.create(**validated_data)
        for movie in movies:
            movie_obj, create = Movies.objects.get_or_create(uuid=movie['uuid'])
            if create:
                movie_obj.title = movie['title']
                movie_obj.description = movie['description']
                '''
                    Genre is splitted and saved in database for future usage.
                    Future usage may include analytical purpose or adding new genre in direct
                '''
                for genre in movie['genres'].split(','):
                    if genre:
                        genre_obj, _ = Genre.objects.get_or_create(name=genre)
                        movie_obj.genres.add(genre_obj)
                movie_obj.save()
            collection_obj.movies.add(movie_obj)
        return collection_obj

    def update(self, obj, validated_data):
        movies = []
        if validated_data.get('movies', None):
            movies = validated_data.pop('movies')
            obj.movies.all().delete()
        obj.title = validated_data.get('title', obj.title)
        obj.description = validated_data.get('description', obj.description)
        for movie in movies:
            movie_obj, create = Movies.objects.get_or_create(uuid=movie['uuid'])
            if create:
                movie_obj.title = movie['title']
                movie_obj.description = movie['description']
                movie_obj.save()
            obj.movies.add(movie_obj)
        return obj

class CollectionMiniSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Collection
        exclude = ('user', 'movies')

class CollectionListSerializer(serializers.ModelSerializer):
    favorite_genres = serializers.SerializerMethodField()
    collections = CollectionMiniSerializer(source='collection_set', many=True)

    class Meta:
        model = User
        fields = ('collections', 'favorite_genres')

    def get_favorite_genres(self, instance):
        '''
            Returns three top most favorited genres from movies saved in collections
        '''
        genre_list = Movies.objects.filter(id__in=list(Collection.objects\
            .filter(user=instance).\
            values_list('movies', flat=True))).\
            values('genres').\
            annotate(count=Count('genres')).\
            order_by('-count')[:3].\
            values_list('genres', flat=True)
        return ','.join(list(Genre.objects.filter(id__in=genre_list)\
            .values_list('name', flat=True)))
        





