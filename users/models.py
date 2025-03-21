from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pseudo = models.CharField(max_length=50, unique=True, verbose_name="Pseudo")

    GENDER_CHOICES = [
        ('man', 'Homme'),
        ('woman', 'Femme'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='man')

    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    pays = models.CharField(max_length=100, blank=True, verbose_name="Pays")
    bio = models.TextField(blank=True, verbose_name="Biographie")
    birthday = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')

    ROLE_CHOICES = [
        ('user', 'Utilisateur'),
        ('admin', 'Administrateur'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'pseudo']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name or self.email
