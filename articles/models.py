from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from articles.validators import validate_body, validate_subheading, validate_title, validate_topic

class Article(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    topic = models.CharField(max_length=20, validators=[validate_topic, RegexValidator(r'^[a-zA-Zà-ù0-9 \-]*$')])
    subheading = models.CharField(max_length=255, validators=[validate_subheading, RegexValidator(r'^[a-zA-Zà-ù0-9 :,.\-]*$',)])
    title = models.CharField(max_length=60, validators=[validate_title,  RegexValidator(r'^[a-zA-Zà-ù0-9 :,.\-]*$',)])
    body = models.TextField(null=False, validators=[validate_body])
    picture = models.ImageField(upload_to='static/', null=True, blank=True)
    likes = models.ManyToManyField(get_user_model(), related_name='liked_articles', blank=True)