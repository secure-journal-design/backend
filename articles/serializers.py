from rest_framework import serializers
from articles.models import Article
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name')

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    num_likes = serializers.SerializerMethodField()
    picture_url = serializers.ImageField(source='picture', read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'author', 'created_at', 'updated_at', 'topic', 'title', 'subheading', 'picture_url','num_likes')
        
    def get_num_likes(self, obj):
        return obj.likes.count()

class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    likes = UserSerializer(many=True, read_only=True)
    picture_url = serializers.ImageField(source='picture', read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'author', 'created_at', 'updated_at', 'topic', 'title', 'subheading', 'body', 'picture_url', 'likes')

class AuthorArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id','topic', 'title', 'subheading', 'body', 'picture')
