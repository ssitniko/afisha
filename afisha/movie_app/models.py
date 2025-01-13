from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    # parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.name


class SearchWords(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    duration = models.IntegerField()
    director = models.ForeignKey('Director', on_delete=models.CASCADE, null=True, related_name='movies')
    search_words = models.ManyToManyField('SearchWords', blank=True)

    def __str__(self):
        return self.title

GRADES = (
    (1, '*'),
    (2, '* *'),
    (3, '* * *'),
    (4, '* * * *'),
    (5, '* * * *'),
)

class Review(models.Model):
    grade = models.IntegerField(choices=GRADES, default=1, null=True)
    text = models.TextField()
    movie = models.ForeignKey('Movie', on_delete=models.SET_NULL, null=True, related_name='reviews')

    def __str__(self):
        return self.text
