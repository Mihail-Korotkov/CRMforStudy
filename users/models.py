from email.mime import image

from django import db
from django.db import models


from django.contrib.auth.models import AbstractUser


# Create your models here.
class Users(AbstractUser):
    email = models.EmailField(unique=True,verbose_name='емайл адрес')
    username = models.CharField(max_length=150, unique=True,verbose_name='имя и фамилия пользователя')
    password = models.CharField(max_length=128,verbose_name='пароль')
    image = models.ImageField(upload_to='users_images', null=True, blank=True, verbose_name='аватарка')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='дата обновления')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        db_table = 'users'

    def __str__(self):
        return self.username
    

class Tasks(models.Model):
    title = models.CharField(max_length=255,verbose_name='название')
    description = models.TextField(verbose_name='описание')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='дата обновления')
    status=models.BooleanField(default=False,verbose_name='статус')

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'
        db_table = 'tasks'

    def __str__(self):
        return self.title
    
class Progress(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE,verbose_name='задача')
    user = models.ForeignKey(Users, on_delete=models.CASCADE,verbose_name='пользователь')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='дата выполнения')

    class Meta:
        verbose_name = 'прогресс'
        verbose_name_plural = 'прогрессы'
        db_table = 'progress'

    def __str__(self):
        return self.task.title
    