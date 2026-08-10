from email.mime import image

from django import db
from django.db import models


from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class Users(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True, verbose_name='аватарка')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='дата обновления')
    role = models.CharField(max_length=255,verbose_name='роль',default='user')
    github_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    telegram_url = models.URLField(max_length=200, blank=True, null=True)

    @property
    def days_on_platform(self):
        """Количество дней на платформе"""
        delta = timezone.now() - self.created_at
        return delta.days
    
    

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        db_table = 'users'
        ordering = ['created_at']

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
    