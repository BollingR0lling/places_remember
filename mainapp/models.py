from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Memory(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    location = models.CharField(max_length=255, null=False)
    title = models.CharField(max_length=50, unique=True, null=False, verbose_name='Воспоминание')
    description = models.TextField(max_length=1024, null=False, verbose_name='Описание')

    def __str__(self):
        return f'{self.user.first_name, self.user.last_name}, воспоминание: {self.title}'
