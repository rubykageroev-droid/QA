# Автотесты — Saucedemo.com

UI и API автотесты на **Python + Playwright + pytest** с архитектурой **Page Object Model**.

---

## Стек

- Python 3.11
- Playwright
- pytest + pytest-playwright
- GitHub Actions (CI/CD)

---

## Структура

```
auto-tests/
├── pages/                    # Page Object Model
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── checkout_step_one.py
│   └── checkout_step_two.py
├── tests/
│   ├── test_ui.py            # UI тесты (saucedemo.com)
│   └── test_api.py           # API тесты (jsonplaceholder)
├── conftest.py               # Фикстуры pytest
└── requirements.txt
```

---

## Покрытие — UI тесты (saucedemo.com)

| Тест | Описание |
|---|---|
| `test_login_valid_user` | Успешная авторизация |
| `test_login_locked_user` | Заблокированный пользователь |
| `test_add_to_cart_and_navigate` | Добавление товара в корзину |
| `test_checkout_with_valid_data` | Оформление заказа с валидными данными |
| `test_checkout_with_minimal_valid_data` | Граничное значение — 1 символ |
| `test_checkout_with_max_length_input` | Граничное значение — максимальная длина |
| `test_checkout_empty_fields_shows_error` | Негативный: пустые поля |
| `test_checkout_complete_full_flow` | E2E: полный flow покупки |
| `test_sort_price_low_to_high` | Сортировка по цене ↑ |
| `test_sort_price_high_to_low` | Сортировка по цене ↓ |
| `test_logout_via_burger_menu` | Выход через бургер-меню |

## Покрытие — API тесты (jsonplaceholder.typicode.com)

| Тест | Метод | Описание |
|---|---|---|
| `test_get_existing_post` | GET | Существующий пост → 200 |
| `test_get_nonexistent_post` | GET | Несуществующий пост → 404 |
| `test_get_post_zero` | GET | ID=0 (граница снизу) → 404 |
| `test_get_post_negative_id` | GET | ID=-1 (негативный) → 404 |
| `test_create_post` | POST | Создание поста → 201 |
| `test_get_comment_499` | GET | Комментарий 499 → 200 |
| `test_get_comment_500` | GET | Комментарий 500 → 200 |
| `test_get_comment_501` | GET | Комментарий 501 → 404 |

---

## Как запустить локально

```bash
# Установить зависимости
pip install -r requirements.txt
playwright install chromium

# Запустить все тесты
pytest tests/ -v

# Только UI
pytest tests/test_ui.py -v

# Только API
pytest tests/test_api.py -v
```

---

## CI/CD

Тесты запускаются автоматически при каждом push в `main` через **GitHub Actions**.
