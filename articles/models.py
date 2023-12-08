from django.db import models
from django.contrib.auth import get_user_model

from articles.validators import validate_body, validate_title, validate_topic

class Article(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    topic = models.CharField(max_length=50, null=False, blank=False, validators=[validate_topic])
    title = models.CharField(max_length=50, null=False, blank=False, validators=[validate_title])
    body = models.TextField(null=False, blank=False, validators=[validate_body])
    likes = models.ManyToManyField(get_user_model(), related_name='liked_articles', blank=True)