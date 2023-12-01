"""Тестирует контент проекта YaNews."""
import pytest
from django.conf import settings
from django.forms import ModelForm
from django.urls import reverse

HOME_URL = reverse('news:home')

pytestmark = pytest.mark.django_db


def test_object_list_in_context(client):
    """Проверь наличие object_list в словаре context."""
    response = client.get(HOME_URL)
    assert 'object_list' in response.context


def test_news_count(client, many_news):
    """Проверь количество новостей на главной странице."""
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, many_news):
    """Проверь сортировку новостей на главной странице."""
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news, few_comments):
    """Проверь сортировку комментариев на странице новости."""
    detail_url = reverse('news:detail', args=(news.id,))
    response = client.get(detail_url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_dates = [all_comments[i].created for i in range(len(all_comments))]
    sorted_dates = sorted(all_dates)
    assert all_dates == sorted_dates


@pytest.mark.parametrize(
    'parametrized_client, form_in_context',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_client_has_or_no_form(form_in_context,
                               news, parametrized_client):
    """Проверь наличие или отсутствие формы редактирования."""
    detail_url = reverse('news:detail', args=(news.id,))
    response = parametrized_client.get(detail_url)
    assert ('form' in response.context) is form_in_context
    if 'form' in response.context:
        assert isinstance(response.context['form'], ModelForm)
