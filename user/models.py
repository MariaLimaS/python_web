from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserModel(AbstractUser):

    TIPO_CHOICES = [("client", "Client"), ("root","Root"),]
    id = models.UUIDField(primary_key= True,
                          default = uuid4,
                          editable=False)

    email=models.EmailField(unique=True)
    suspenso = models.BooleanField(default=False)
    tipo = models.CharField (max_length=10, choices=TIPO_CHOICES, default="client")