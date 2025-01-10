from rest_framework import serializers
from .models import Movie, Director, Review, SearchWords


class MovieSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    reviews_rating = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        # fields = 'title description duration director'.split()
        fields = 'title description duration director search_words reviews reviews_rating'.split()
        # exclude = 'duration director'.split() # не работает с fields = '__all__' параллельно
        # depth = 1

    def get_reviews(self, movie):
        reviews = movie.reviews.all()
        return ReviewSerializer(reviews, many=True).data

    def get_reviews_rating(self, movie):
        reviews = movie.reviews.all()
        grades = reviews.values_list('grade', flat=True)
        if grades:
            return round(sum(grades) / len(grades))
        return None


class DirectorSerializer(serializers.ModelSerializer):
    # movies = serializers.SerializerMethodField()
    movies_count = serializers.SerializerMethodField()
    class Meta:
        model = Director
        fields = 'name movies_count'.split()
        # fields = 'name movies movies_count'.split()
        # depth = 1

    def get_movies(self, obj):
        movies = obj.movies.all()
        return MovieSerializer(movies, many=True).data

    def get_movies_count(self, obj):
        return obj.movies.count()



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'grade text movie'.split()




class SearchWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchWords
        fields = '__all__'
