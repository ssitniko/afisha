from gettext import textdomain
from logging import raiseExceptions

from django.core.serializers import serialize
from rest_framework.generics import ListAPIView
from django.db import transaction
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Director, Review, SearchWords
from .serializers import (MovieSerializer, DirectorSerializer, ReviewSerializer, MovieItemSerializer,
                          DirectorItemSerializer, ReviewItemSerializer, MovieValidateSerializer,
                          DirectorValidateSerializer, ReviewValidateSerializer, SearchWordSerializer)
from rest_framework.viewsets import ModelViewSet



class DirectorListAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'

class SearchWordsViewSet(ModelViewSet):
    queryset = SearchWords.objects.all()
    serializer_class = SearchWordSerializer

class MovieListCreateAPIView(ListCreateAPIView):
    queryset = Movie.objects.select_related('director').prefetch_related('search_words', 'reviews').all()
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director_id = serializer.validated_data.get('director_id')
        search_words = serializer.validated_data.get('search_words')

        with transaction.atomic():
            movie = Movie.objects.create(
                title=title,
                description=description,
                duration=duration,
                director_id=director_id,
            )
            movie.search_words.set(search_words)
            movie.save()
        return Response(status=status.HTTP_201_CREATED, data=MovieItemSerializer(movie).data)

class MovieDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'


class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


# function methods are below
#====================================================================================================
@api_view(http_method_names=['GET','POST'])
def movie_list_api_view(request):
    # movies = Movie.objects.all()
    print(request.user)
    if request.method == 'GET':
        movies = Movie.objects.select_related('director').prefetch_related('search_words', 'reviews').all()

        # list_ = MovieSerializer(instance=movies, many=True).data
        data = MovieSerializer(instance=movies, many=True).data
        # return Response(data=list_)
        return Response(data=data)

    elif request.method == 'POST':
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director_id = serializer.validated_data.get('director_id')
        search_words = serializer.validated_data.get('search_words')

        with transaction.atomic():
            movie = Movie.objects.create(
                title=title,
                description=description,
                duration=duration,
                director_id=director_id,
            )
            movie.search_words.set(search_words)
            movie.save()
        return Response(status=status.HTTP_201_CREATED, data=MovieItemSerializer(movie).data)


@api_view(http_method_names=['GET', 'POST'])
def director_list_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()

        data = DirectorSerializer(directors, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        name = serializer.validated_data.get('name')

        director = Director.objects.create(
            name=name,
        )
        return Response(status=status.HTTP_201_CREATED, data=DirectorItemSerializer(director).data)

    # list_ = []
    # for i in directors:
    #     list_.append({
    #         'name': i.name,
    #     })
    # return Response(data=list_)



@api_view(http_method_names=['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data)

    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        grade = serializer.validated_data.get('grade')
        text = serializer.validated_data.get('text')
        movie_id = serializer.validated_data.get('movie')


        review = Review.objects.create(
            grade=grade,
            text=text,
            movie_id=movie_id,
        )
        return Response(status=status.HTTP_201_CREATED, data=ReviewItemSerializer(review).data)



@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Movie not found!'})
    if request.method == 'GET':
        data = MovieSerializer(instance=movie).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.director = serializer.validated_data.get('director')
        movie.search_words.set(serializer.validated_data.get('search_words'))
        movie.save()
        return Response(data=MovieItemSerializer(movie).data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Director not found!'})
    if request.method == 'GET':
        data = DirectorSerializer(instance=director).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        director.name = serializer.validated_data.get('name')
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Review not found!'})
    if request.method == 'GET':
        data = ReviewSerializer(instance=review).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        review.grade = serializer.validated_data.get('grade')
        review.text = serializer.validated_data.get('text')
        review.movie = serializer.validated_data.get('movie')

        return Response(data=ReviewItemSerializer(review).data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


