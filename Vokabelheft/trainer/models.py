from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Parts(models.Model):
    name = models.CharField(max_length=50, help_text="Введите часть речи", verbose_name="Parts")

    def __str__(self):
        return self.name


class Dictionaries(models.Model):
    name = models.CharField(max_length=25, help_text="Введите название языка", verbose_name="Language")

    def __str__(self):
        return self.name


class Dictionary(models.Model):
    key = models.CharField(max_length=100, help_text="Введите иностранное слово",
                           verbose_name="Foreign word")
    keyfonetic = models.CharField(max_length=100, help_text="Веведите фонетику слова", blank=True,
                                  verbose_name="Fonetic of word")
    word = models.CharField(max_length=150, help_text="Перевод", verbose_name="Translate")
    form = models.CharField(max_length=100, help_text="Формы глагола", verbose_name="Forms of verb",
                            blank=True)
    plural = models.CharField(max_length=100, help_text="Множественное число", verbose_name="Plural",
                              blank=True)
    part = models.ForeignKey(Parts, null=True, on_delete=models.SET_NULL, help_text="Введите часть речи", verbose_name="Part")
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    language = models.ForeignKey(Dictionaries, on_delete=models.CASCADE)
    moderate = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.key

    def get_absolute_url(self):
        return reverse('dictionary-detail', args=[str(self.id)])




