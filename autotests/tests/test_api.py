import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture
def api(playwright):
    """API контекст для всех тестов"""
    context = playwright.request.new_context(base_url=BASE_URL)
    yield context
    context.dispose()


# ──────────────────────────────────────────────
# GET запросы — посты
# ──────────────────────────────────────────────

def test_get_existing_post(api):
    """Получение существующего поста возвращает 200 и корректные данные"""
    response = api.get("/posts/1")

    assert response.status == 200

    data = response.json()
    assert data["id"] == 1
    assert "title" in data
    assert len(data["title"]) > 0


def test_get_nonexistent_post(api):
    """Несуществующий пост возвращает 404"""
    response = api.get("/posts/9999")

    assert response.status == 404


def test_get_post_zero(api):
    """Пост с ID=0 (граничное значение снизу) возвращает 404"""
    response = api.get("/posts/0")

    assert response.status == 404


def test_get_post_negative_id(api):
    """Пост с отрицательным ID возвращает 404"""
    response = api.get("/posts/-1")

    assert response.status == 404


# ──────────────────────────────────────────────
# POST запросы
# ──────────────────────────────────────────────

def test_create_post(api):
    """Создание нового поста возвращает 201 и данные с ID"""
    payload = {
        "title": "Тестовый заголовок",
        "body": "Тело поста",
        "userId": 1
    }

    response = api.post("/posts", data=payload)

    assert response.status == 201

    data = response.json()
    assert "id" in data
    assert data["title"] == "Тестовый заголовок"


# ──────────────────────────────────────────────
# Граничные значения — комментарии (всего 500)
# ──────────────────────────────────────────────

def test_get_comment_499(api):
    """Комментарий 499 — внутри допустимого диапазона, возвращает 200"""
    response = api.get("/comments/499")

    assert response.status == 200


def test_get_comment_500(api):
    """Комментарий 500 — последний валидный, возвращает 200"""
    response = api.get("/comments/500")

    assert response.status == 200


def test_get_comment_501(api):
    """Комментарий 501 — за пределами диапазона, возвращает 404"""
    response = api.get("/comments/501")

    assert response.status == 404
