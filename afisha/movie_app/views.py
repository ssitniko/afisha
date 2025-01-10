from logging import raiseExceptions

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Director, Review
from .serializers import MovieSerializer, DirectorSerializer, ReviewSerializer

@api_view(http_method_names=['GET'])
def movie_list_api_view(request):
    movies = Movie.objects.all()

    list_ = MovieSerializer(instance=movies, many=True).data

    # list_ = []
    # for i in movies:
    #     list_.append({
    #         'title': i.title,
    #         'description': i.description,
    #         'duration': i.duration,
    #         'director': str(i.director),
    #     })
    return Response(data=list_)

@api_view(http_method_names=['GET'])
def director_list_api_view(request):
    directors = Director.objects.all()

    data = DirectorSerializer(directors, many=True).data
    return Response(data=data)
    # list_ = []
    # for i in directors:
    #     list_.append({
    #         'name': i.name,
    #     })
    # return Response(data=list_)



@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    list_ = []
    for i in reviews:
        list_.append({
            'text': i.text,
            'movie': str(i.movie),
            'grade': i.grade,
        })
    return Response(data=list_)

@api_view(['GET'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Movie not found!'})
    data = MovieSerializer(instance=movie).data
    return Response(data=data)

@api_view(['GET'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Director not found!'})
    data = DirectorSerializer(instance=director).data
    return Response(data=data)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Review not found!'})
    data = ReviewSerializer(instance=review).data
    return Response(data=data)


