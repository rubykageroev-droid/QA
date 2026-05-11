import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_step_one import CheckoutStepOne
from pages.checkout_step_two import CheckoutStepTwo


# ──────────────────────────────────────────────
# АВТОРИЗАЦИЯ
# ──────────────────────────────────────────────

def test_login_valid_user(page):
    """Успешная авторизация валидным пользователем"""
    login = LoginPage(page)
    page.goto("https://www.saucedemo.com")
    login.login("standard_user", "secret_sauce")

    assert page.locator(".title").text_content() == "Products"


def test_login_locked_user(page):
    """Заблокированный пользователь получает ошибку"""
    login = LoginPage(page)
    page.goto("https://www.saucedemo.com")
    login.login("locked_out_user", "secret_sauce")

    error = page.locator("[data-test='error']")
    assert error.text_content() == "Epic sadface: Sorry, this user has been locked out."


# ──────────────────────────────────────────────
# КОРЗИНА
# ──────────────────────────────────────────────

def test_add_to_cart_and_navigate(logged_in_page):
    """Добавление товара и переход в корзину"""
    inventory = InventoryPage(logged_in_page)
    inventory.add_backpack()
    inventory.go_to_cart()

    assert "cart.html" in logged_in_page.url


# ──────────────────────────────────────────────
# ОФОРМЛЕНИЕ ЗАКАЗА
# ──────────────────────────────────────────────

def test_checkout_with_valid_data(cart_ready_page):
    """Оформление заказа с валидными данными"""
    inventory = InventoryPage(cart_ready_page)
    checkout = CheckoutStepOne(cart_ready_page)

    inventory.checkout()
    checkout.order("Alex", "Fishuk", "222222")

    assert "checkout-step-two.html" in cart_ready_page.url


def test_checkout_with_minimal_valid_data(cart_ready_page):
    """Оформление заказа с минимальными валидными данными (1 символ)"""
    inventory = InventoryPage(cart_ready_page)
    checkout = CheckoutStepOne(cart_ready_page)

    inventory.checkout()
    checkout.order("A", "S", "1")

    assert "checkout-step-two.html" in cart_ready_page.url


def test_checkout_with_max_length_input(cart_ready_page):
    """Оформление заказа с максимальной длиной ввода (граничное значение)"""
    inventory = InventoryPage(cart_ready_page)
    checkout = CheckoutStepOne(cart_ready_page)

    inventory.checkout()
    checkout.order(
        "A" * 47,
        "S" * 35,
        "2" * 35,
    )

    assert "checkout-step-two.html" in cart_ready_page.url


def test_checkout_empty_fields_shows_error(cart_ready_page):
    """Пустые поля на checkout показывают ошибку"""
    inventory = InventoryPage(cart_ready_page)
    checkout = CheckoutStepOne(cart_ready_page)

    inventory.checkout()
    checkout.order("", "", "")

    error = cart_ready_page.locator("[data-test='error']")
    assert error.text_content() == "Error: First Name is required"


def test_checkout_complete_full_flow(cart_ready_page):
    """Полный E2E flow: корзина → данные → финиш"""
    inventory = InventoryPage(cart_ready_page)
    checkout_one = CheckoutStepOne(cart_ready_page)
    checkout_two = CheckoutStepTwo(cart_ready_page)

    inventory.checkout()
    checkout_one.order("Alex", "Fishuk", "222222")
    checkout_two.finish()

    assert "checkout-complete.html" in cart_ready_page.url


# ──────────────────────────────────────────────
# СОРТИРОВКА
# ──────────────────────────────────────────────

def test_sort_price_low_to_high(logged_in_page):
    """Сортировка товаров по цене: от низкой к высокой"""
    logged_in_page.goto("https://www.saucedemo.com/inventory.html")
    inventory = InventoryPage(logged_in_page)
    inventory.select_sort("lohi")

    prices_raw = inventory.item_prices.all_text_contents()
    prices = [float(p.replace("$", "")) for p in prices_raw]

    assert prices == sorted(prices), f"Ожидали по возрастанию: {sorted(prices)}, получили: {prices}"


def test_sort_price_high_to_low(logged_in_page):
    """Сортировка товаров по цене: от высокой к низкой"""
    logged_in_page.goto("https://www.saucedemo.com/inventory.html")
    inventory = InventoryPage(logged_in_page)
    inventory.select_sort("hilo")

    prices_raw = inventory.item_prices.all_text_contents()
    prices = [float(p.replace("$", "")) for p in prices_raw]

    assert prices == sorted(prices, reverse=True), f"Ожидали по убыванию: {sorted(prices, reverse=True)}, получили: {prices}"


# ──────────────────────────────────────────────
# ВЫХОД
# ──────────────────────────────────────────────

def test_logout_via_burger_menu(logged_in_page):
    """Выход из аккаунта через бургер-меню"""
    logged_in_page.goto("https://www.saucedemo.com/inventory.html")
    inventory = InventoryPage(logged_in_page)
    inventory.logoutburger()

    assert logged_in_page.locator("#login-button").is_visible()
