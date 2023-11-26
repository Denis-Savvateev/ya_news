"""Тестирует логику проекта YaNews."""


def test_anonymous_user_cant_create_comment():
    """Проверь возможность анонима создавать комментарии."""
    ...


def test_user_can_create_comment():
    """Проверь возможность пользователя создать комментарий."""
    ...


def test_user_cant_use_bad_words():
    """Проверь невозможность отправки дурных слов."""
    ...


def test_author_can_delete_comment():
    """Проверь возможность автора удалить комментарий."""
    ...


def test_user_cant_delete_comment_of_another_user():
    """Проверь невозможность пользователя удалить чужой комментарий."""
    ...


def test_author_can_edit_comment():
    """Проверь возможность автора править комментарий."""
    ...


def test_user_cant_edit_comment_of_another_user():
    """Проверь невозможность пользователя править чужой комментарий."""
    ...
