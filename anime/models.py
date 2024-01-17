from django.db import models
from .constants import *


class HashTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Anime(models.Model):
    title = models.CharField(max_length=125, verbose_name='Название')
    card_image = models.ImageField(upload_to='card_images/', blank=True, null=True, verbose_name='Изображение карт')
    rate = models.IntegerField(choices=RATING_TYPES, default=0, verbose_name='Оценка')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обнавления')
    category = models.CharField(choices=CATEGORY_TYPES, max_length=10, default='kids', verbose_name='Категория')
    url = models.URLField(null=True, blank=True, verbose_name='Видео')
    hashtags = models.ManyToManyField(HashTag, related_name='animes')

    def __str__(self):
        return self.title


class Comment(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return f'{self.anime.title} - {self.text}'