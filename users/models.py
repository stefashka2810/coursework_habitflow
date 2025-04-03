from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import BaseUserManager


class User(AbstractUser):
    
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['last_name', 'first_name']

    def get_display_name(self):
        full_name = self.get_full_name().strip()
        return full_name if full_name else self.username
    
    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'

