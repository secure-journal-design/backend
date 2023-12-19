import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.status import *
from rest_framework.test import APIClient
from django.contrib.auth.models import Group

from articles.models import Article

@pytest.fixture()
def articles(db):
    return [mixer.blend('articles.Article') for _ in range(3)]

@pytest.fixture()
def article_editors_group(db):
    group, created = Group.objects.get_or_create(name='article_editors')
    return group

@pytest.fixture()
def user_in_article_editors_group(article_editors_group):
    user = mixer.blend(get_user_model())
    user.groups.add(article_editors_group)
    return user


def get_client(user=None):
    res = APIClient()
    if user is not None:
        res.force_login(user)
    return res


def parse(response):
    response.render()
    content = response.content.decode()
    return json.loads(content)

"""
def contains(response, key, value):
    obj = parse(response)
    if key not in obj:
        return False
    return value in obj[key]
"""
def test_article_anon_user_get_articles_list(articles):
    path = reverse('articles-list')
    user = mixer.blend(get_user_model())
    client = get_client(user)
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == len(articles)

def test_article_retrieve_a_single_article(articles):
    path = reverse('articles-detail', kwargs={'pk': articles[0].pk})
    client = get_client(articles[0].author)
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert obj['title'] == articles[0].title

def test_article_anon_user_cannot_add_article(db):
    path = reverse('article-editors-list')
    client = get_client()
    response = client.post(path, data={'title': 'Title', 'subheading':'Subheading', 'topic':'Topic', 'body':'Bodyyyyyyyyyyyyyyyyyyyyy'})
    assert response.status_code == HTTP_401_UNAUTHORIZED

def test_article_retrieve_by_topic(articles):
    path = reverse('articles-by-topic')
    topic_name = articles[0].topic
    client = get_client()
    response = client.get(path, {'topic': topic_name})
    obj = parse(response)
    assert response.status_code == HTTP_200_OK
    assert obj[0]['title'] == articles[0].title

def test_article_retrieve_by_topic_without_topic_param(db):
    path = reverse('articles-by-topic')
    client = get_client()
    response = client.get(path)
    obj = parse(response)
    assert response.status_code == HTTP_400_BAD_REQUEST

def test_article_authenticated_user_can_like_article(articles):
    path = reverse('articles-like', kwargs={'pk': articles[0].pk})
    user = mixer.blend(get_user_model())
    client = get_client(user)
    response = client.post(path)
    assert response.status_code == HTTP_200_OK
    #obj = parse(response)
    #assert obj['detail'] == 'Article liked successfully.'

def test_article_anon_user_cannot_like_article(articles):
    path = reverse('articles-like', kwargs={'pk': articles[0].pk})
    client = get_client()
    response = client.post(path)
    assert response.status_code == HTTP_401_UNAUTHORIZED

def test_article_user_cannot_like_not_existing_article(articles):
    path = reverse('articles-like', kwargs={'pk': 10})
    user = mixer.blend(get_user_model())
    client = get_client(user)
    response = client.post(path)
    assert response.status_code == HTTP_404_NOT_FOUND

def test_article_editor_can_create_article(user_in_article_editors_group):
    path = reverse('article-editors-list')
    client = get_client(user_in_article_editors_group)
    data = {'title': 'Title', 'subheading': 'Subheading', 'topic': 'Topic', 'body': 'Bodyyyyyyyyyyyyyyyyyyyyy'}
    response = client.post(path, data=data)
    assert response.status_code == HTTP_201_CREATED
    assert Article.objects.filter(author=user_in_article_editors_group).exists()

def test_article_editor_can_get_article(user_in_article_editors_group, articles):
    article = articles[0]
    path = reverse('article-editors-detail', kwargs={'pk': article.pk})
    client = get_client(user_in_article_editors_group)
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert obj['title'] == article.title

def test_article_editor_can_get_articles(user_in_article_editors_group, articles):
    path = reverse('article-editors-list')
    client = get_client(user_in_article_editors_group)
    response = client.get(path)
    assert response.status_code == HTTP_200_OK
    obj = parse(response)
    assert len(obj) == len(articles)

def test_article_retrieve_by_author(articles):
    path = reverse('articles-by-author')
    topic_name = articles[0].author.username
    client = get_client()
    response = client.get(path, {'author': topic_name})
    obj = parse(response)
    assert response.status_code == HTTP_200_OK
    assert obj[0]['title'] == articles[0].title

def test_article_retrieve_by_author_without_author_param(db):
    path = reverse('articles-by-author')
    client = get_client()
    response = client.get(path)
    obj = parse(response)
    assert response.status_code == HTTP_400_BAD_REQUEST