from django.contrib import admin
from .models import Movie, Director, Review, SearchWords

admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Review)
admin.site.register(SearchWords)