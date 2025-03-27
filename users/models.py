from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    username = None
    
    age = models.PositiveIntegerField(
        _('Age'),
        validators=[
            MinValueValidator(6),
            MaxValueValidator(120)
        ],
        blank=True,
        null=True
    )

    gender = models.CharField(
        _('Gender'),
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True, 
        null=True
    )

    email = models.EmailField(
        _('Email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )


    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
