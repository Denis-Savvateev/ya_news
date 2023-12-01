"""Тестирует маршруты проекта YaNews."""

from http import HTTPStatus

from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('home_url'),
        pytest.lazy_fixture('news_url'),
        pytest.lazy_fixture('login_url'),
        pytest.lazy_fixture('logout_url'),
        pytest.lazy_fixture('signup_url'),
    )
)
def test_pages_availability_for_anonymous_user(client, url):
    """Проверь доступность для всех пользователей нужных страниц."""
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user_client, status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_availability_for_comment_edit_and_delete(comment, name, status,
                                                  user_client):
    """Проверь доступность страниц редактированияи/удаления комментария."""
    url = reverse(name, args=(comment.id,))
    response = user_client.get(url)
    assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_redirect_for_anonymous_client(client, comment, name):
    """Проверь перенаправление анонимного пользователя."""
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
