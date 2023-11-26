"""Фикстуры для пакета pytest."""

from datetime import datetime, timedelta

import pytest

from django.conf import settings
from django.utils import timezone
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    """Создай фикстуру автора записи."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def reader(django_user_model):
    """Создай фикстуру читателя записи."""
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def author_client(author, client):
    """Создай фикстуру клиента, авторизованного для пользователя автора."""
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader, client):
    """Создай фикстуру клиента, авторизованного для пользователя-читателя."""
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    """Создай запись новости в базе данных."""
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news


@pytest.fixture
def many_news():
    """Создай несколько записей новостей в базе данных."""
    today = datetime.today()
    many_news = News.objects.bulk_create(
            News(
                title=f'Новость {index}',
                text='Просто текст.',
                date=today - timedelta(days=index)
            )
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return many_news


@pytest.fixture
def comment(news, author):
    """Создай запись комментария от автора к новости."""
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Комментарий',
    )
    return comment


@pytest.fixture
def many_comments(news, author):
    """Создай несколько записей комментариев от автора к новости."""
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
        many_comments = Comment.objects.all()
    return many_comments


@pytest.fixture
def news_id(news):
    """Верни параметр id для записи новости."""
    return news.id,


# @pytest.fixture
# def comment_id(comment):
#     """Верни параметр id для записи комментария."""
#     return comment.id,
