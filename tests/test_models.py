import pytest
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer

def test_title_must_be_at_least_3_characters_long(db):
    article = mixer.blend('articles.Article', title='ab')
    with pytest.raises(ValidationError):
        article.full_clean()

def test_body_must_be_at_least_3_characters_long(db):
    article = mixer.blend('articles.Article', body='ab')
    with pytest.raises(ValidationError):
        article.full_clean()

def test_topic_must_be_at_least_3_characters_long(db):
    article = mixer.blend('articles.Article', topic='ab')
    with pytest.raises(ValidationError):
        article.full_clean()