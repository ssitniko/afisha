from gettext import textdomain
from logging import raiseExceptions

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Director, Review
from .serializers import (MovieSerializer, DirectorSerializer, ReviewSerializer, MovieItemSerializer,
                          DirectorItemSerializer, ReviewItemSerializer)

@api_view(http_method_names=['GET','POST'])
def movie_list_api_view(request):
    # movies = Movie.objects.all()
    if request.method == 'GET':
        movies = Movie.objects.select_related('director').prefetch_related('search_words', 'reviews').all()

        # list_ = MovieSerializer(instance=movies, many=True).data
        data = MovieSerializer(instance=movies, many=True).data
        # return Response(data=list_)
        return Response(data=data)

    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')
        search_words = request.data.get('search_words')

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
        name = request.data.get('name')

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
        grade = request.data.get('grade')
        text = request.data.get('text')
        movie_id = request.data.get('movie_id')

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
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director = request.data.get('director')
        movie.search_words.set(request.data.get('search_words'))
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
        director.name = request.data.get('name')
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
        review.grade = request.data.get('grade')
        review.text = request.data.get('text')
        review.movie = request.data.get('movie')

        return Response(data=ReviewItemSerializer(review).data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


