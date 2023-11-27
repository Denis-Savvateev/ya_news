"""Фикстуры для пакета pytest."""

from datetime import datetime, timedelta

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import pytest

from news.models import Comment, News
from news.pytest_tests.const import COMMENT_TEXT


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
        text=COMMENT_TEXT,
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


@pytest.fixture
def news_url(news):
    """Верни url новости."""
    news_url = reverse('news:detail', args=(news.id,))
    return news_url


@pytest.fixture
def edit_url(comment):
    """Верни url редактирования комментария."""
    edit_url = reverse('news:edit', args=(comment.id,))
    return edit_url


@pytest.fixture
def delete_url(comment):
    """Верни url удаления комментария."""
    delete_url = reverse('news:delete', args=(comment.id,))
    return delete_url


@pytest.fixture
def url_to_comments(news_url):
    """Верни url комментария."""
    url_to_comments = news_url + '#comments'
    return url_to_comments
