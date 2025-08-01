from django.db import models

from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class Document(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(default='Title', max_length=255)
    content = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)