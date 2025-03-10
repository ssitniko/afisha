# Generated by Django 5.1.4 on 2025-01-09 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchWords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='director',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movie_app.director'),
        ),
        migrations.AddField(
            model_name='review',
            name='grade',
            field=models.IntegerField(choices=[(1, '*'), (2, '* *'), (3, '* * *'), (4, '* * * *'), (5, '* * * * *')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='movie_app.movie'),
        ),
        migrations.AddField(
            model_name='movie',
            name='search_words',
            field=models.ManyToManyField(blank=True, to='movie_app.searchwords'),
        ),
    ]
