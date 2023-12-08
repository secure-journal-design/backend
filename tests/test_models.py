import pytest
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer

@pytest.mark.django_db
def test_title_must_be_at_least_3_characters_long():
    article = mixer.blend('articles.Article', title='ab')
    with pytest.raises(ValidationError):
        article.full_clean()

@pytest.mark.django_db
def test_body_must_be_at_least_3_characters_long():
    article = mixer.blend('articles.Article', body='ab')
    with pytest.raises(ValidationError):
        article.full_clean()

@pytest.mark.django_db
def test_topic_must_be_at_least_3_characters_long():
    article = mixer.blend('articles.Article', topic='ab')
    with pytest.raises(ValidationError):
        article.full_clean()