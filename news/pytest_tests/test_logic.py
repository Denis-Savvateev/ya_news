"""Тестирует логику проекта YaNews."""

from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.const import COMMENT_TEXT, NEW_COMMENT_TEXT

form_data = {'text': COMMENT_TEXT}
form_new_data = {'text': NEW_COMMENT_TEXT}


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news_url):
    """Проверь возможность анонима создавать комментарии."""
    client.post(news_url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(author_client, news,  news_url, author):
    """Проверь возможность пользователя создать комментарий."""
    response = author_client.post(news_url, data=form_data)
    assertRedirects(response, f'{news_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, news_url):
    """Проверь невозможность отправки дурных слов."""
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(news_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user_client, status, count, redirect',
    (
        (pytest.lazy_fixture('author_client'), None,
         0, pytest.lazy_fixture('url_to_comments')),
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND,
         1, None),
    )
)
def test_author_can_delete_comment(
    user_client,
    status,
    count,
    redirect,
    delete_url
):
    """Проверь возможность пользователей удалить комментарий."""
    response = user_client.delete(delete_url)
    if redirect:
        assertRedirects(response, redirect)
    comments_count = Comment.objects.count()
    if status:
        assert response.status_code == status
    assert comments_count == count


@pytest.mark.django_db
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
    response = user_client.post(edit_url, data=form_new_data)
    if redirect:
        assertRedirects(response, redirect)
    if status:
        assert response.status_code == status
    comment.refresh_from_db()
    assert comment.text == text
