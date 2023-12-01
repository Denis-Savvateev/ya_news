"""Тестирует логику проекта YaNews."""

from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.const import (
    COMMENT_TEXT,
    NEW_COMMENT_TEXT,
    FORM_DATA,
    FORM_NEW_DATA
)

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, news_url):
    """Проверь возможность анонима создавать комментарии."""
    comments_count_before = Comment.objects.count()
    client.post(news_url, data=FORM_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == comments_count_before


def test_user_can_create_comment(author_client, news, news_url, author):
    """Проверь возможность пользователя создать комментарий."""
    Comment.objects.all().delete()
    comments_count_before = Comment.objects.count()
    response = author_client.post(news_url, data=FORM_DATA)
    assertRedirects(response, f'{news_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == comments_count_before + 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize(
    'bad_word',
    (bad_word for bad_word in BAD_WORDS)
)
def test_user_cant_use_bad_words(author_client, bad_word, news_url):
    """Проверь невозможность отправки дурных слов."""
    bad_words_data = {'text': f'Какой-то текст, {bad_word}, еще текст'}
    response = author_client.post(news_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )


@pytest.mark.parametrize(
    'user_client, status, is_changed, redirect',
    (
        (pytest.lazy_fixture('author_client'), None,
         True, pytest.lazy_fixture('url_to_comments')),
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND,
         False, None),
    )
)
def test_user_can_delete_comment(
    user_client,
    status,
    is_changed,
    redirect,
    delete_url
):
    """Проверь возможность пользователей удалить комментарий."""
    comments_before = str(Comment.objects.all())
    response = user_client.post(delete_url)
    comments = str(Comment.objects.all())
    if redirect:
        assertRedirects(response, redirect)
    if status:
        assert response.status_code == status
    table_status = (comments_before != comments)
    assert table_status == is_changed


@pytest.mark.parametrize(
    'user_client, status, text, redirect',
    (
        (pytest.lazy_fixture('author_client'), None,
         NEW_COMMENT_TEXT, pytest.lazy_fixture('url_to_comments')),
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND,
         COMMENT_TEXT, None),
    )
)
def test_author_can_edit_comment(
        user_client,
        status,
        text,
        redirect,
        comment,
        edit_url,
):
    """Проверь возможность пользователей править комментарий."""
    news_before = comment.news
    author_before = comment.author
    created_before = comment.created
    response = user_client.post(edit_url, data=FORM_NEW_DATA)
    if redirect:
        assertRedirects(response, redirect)
    if status:
        assert response.status_code == status
        assert comment.news == news_before
        assert comment.author == author_before
        assert comment.created == created_before
    comment.refresh_from_db()
    assert comment.text == text
