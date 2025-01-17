from rest_framework import serializers
from .models import Movie, Director, Review, SearchWords
from rest_framework.exceptions import ValidationError


class MovieItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class DirectorItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class ReviewItemSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    class Meta:
        model = Review
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    reviews_rating = serializers.SerializerMethodField()
    class Meta:
        model = Movie

        fields = 'title description duration director search_words reviews reviews_rating'.split()
        # exclude = 'duration director'.split() # не работает с fields = '__all__' параллельно
        # depth = 1

    def get_reviews(self, movie):
        reviews = movie.reviews.all()
        return ReviewSerializer(reviews, many=True).data

    def get_reviews_rating(self, movie):
        reviews = movie.reviews.all()
        grades = [review.grade for review in movie.reviews.all()]
        if grades:
            return round(sum(grades) / len(grades))
        return None

class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255, min_length=5)
    description = serializers.CharField(required=False, default= 'no description')
    duration = serializers.IntegerField()
    director = serializers.IntegerField()
    # director = serializers.ChoiceField(choices=[1, 2, 3])
    search_words = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_director(self, director):
        try:
            Director.objects.get(id=director)
        except:
            raise ValidationError("Director doesn't exist")
        return director

    def validate_search_words(self, search_words):
        search_words_db = SearchWords.objects.filter(id__in=search_words)
        existing_id = [i.id for i in search_words_db]
        missing_word = [i for i in search_words if i not in existing_id]

        if missing_word:
            raise ValidationError(f"SearchWord(s) {missing_word} do not exist!")

        return search_words



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


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255, min_length=1)

    def validate_name(self, name):
        name_db = Director.objects.filter(name=name)
        if name_db.exists():
            raise ValidationError(f" Director with name {name} already exists!")
        return name



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'grade text movie'.split()


class ReviewValidateSerializer(serializers.Serializer):
    grade = serializers.ChoiceField(choices=[1, 2, 3, 4, 5])
    text = serializers.CharField(required=True)
    movie = serializers.IntegerField()


    def validate_movie(self, movie):
        try:
            Movie.objects.get(id=movie)
        except:
            raise ValidationError("Movie does not exist!")
        return movie

    def validate_text(self, text):
        if not text.strip():
            raise serializers.ValidationError("The review text cannot be empty or contain only spaces.")
        elif len(text) < 10:
            raise serializers.ValidationError("The review text is too short. Minimum 10 characters.")
        elif len(text) > 500:
            raise serializers.ValidationError("The review text is too long. Maximum 500 characters.")
        return text

    # def validate_search_words(self, search_words):
    #     search_words_db = SearchWords.objects.filter(id__in=search_words)
    #     existing_id = [i.id for i in search_words_db]
    #     missing_word = [i for i in search_words if i not in existing_id]
    #
    #     if missing_word:
    #         raise ValidationError(f"SearchWord(s) {missing_word} do not exist!")
    #
    #     return search_words



class SearchWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchWords
        fields = '__all__'


