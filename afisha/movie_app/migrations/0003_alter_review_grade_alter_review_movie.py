# Generated by Django 5.1.4 on 2025-01-09 11:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0002_searchwords_director_parent_review_grade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='grade',
            field=models.IntegerField(choices=[(1, '*'), (2, '* *'), (3, '* * *'), (4, '* * * *'), (5, '* * * *')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movie_app.movie'),
        ),
    ]
