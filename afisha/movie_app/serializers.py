from rest_framework import serializers
from .models import Movie, Director, Review


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # fields = 'title description duration director'.split()
        fields = '__all__' # вывод всех полей
        # exclude = 'duration director'.split() # не работает с fields = '__all__' параллельно

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'