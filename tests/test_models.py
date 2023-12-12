import pytest
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer

def test_title_must_be_at_least_5_characters_long(db):
    article = mixer.blend('articles.Article', title='ab')
    with pytest.raises(ValidationError):
        article.full_clean()

def test_body_must_be_at_least_20_characters_long(db):
    article = mixer.blend('articles.Article', body='ab')
    with pytest.raises(ValidationError):
        article.full_clean()

def test_topic_must_be_at_least_3_characters_long(db):
    article = mixer.blend('articles.Article', topic='ab')
    with pytest.raises(ValidationError):
        article.full_clean()

def test_subheading_must_be_at_least_5_characters_long(db):
    article = mixer.blend('articles.Article', subheading='ab')
    with pytest.raises(ValidationError):
        article.full_clean()

def test_topic_must_be_at_most_20_characters_long(db):
    article = mixer.blend('articles.Article', topic='a' * 21)
    with pytest.raises(ValidationError):
        article.full_clean()

def test_subheading_must_be_at_most_255_characters_long(db):
    article = mixer.blend('articles.Article', subheading='a' * 256)
    with pytest.raises(ValidationError):
        article.full_clean()

def test_title_must_be_at_most_60_characters_long(db):
    article = mixer.blend('articles.Article', title='a' * 61)
    with pytest.raises(ValidationError):
        article.full_clean()

def test_body_must_be_at_most_1000_characters_long(db):
    article = mixer.blend('articles.Article', body='a' * 1001)
    with pytest.raises(ValidationError):
        article.full_clean()

def test_valid_topic(db):
    article = mixer.blend('articles.Article', topic = 'ValidTopic123 ')
    article.full_clean()

def test_invalid_topic(db):
    article = mixer.blend('articles.Article', topic = 'InvalidTopic123 -@')
    with pytest.raises(ValidationError):
        article.full_clean()

def test_valid_subheading(db):
    article = mixer.blend('articles.Article', subheading = "ValidSubheading123 ,.-")
    article.full_clean()

def test_invalid_subheading(db):
    article = mixer.blend('articles.Article', subheading = 'InvalidSubheading123 ,.-@')
    with pytest.raises(ValidationError):
        article.full_clean()

def test_valid_title(db):
    article = mixer.blend('articles.Article', title = 'ValidTitle123 ,.-')
    article.full_clean()

def test_invalid_title(db):
    article = mixer.blend('articles.Article', title = 'InvalidTitle123 ,.-@')
    with pytest.raises(ValidationError):
        article.full_clean()
