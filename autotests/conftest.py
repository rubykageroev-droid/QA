import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def logged_in_page(page):
    """Страница с уже авторизованным пользователем"""
    from pages.login_page import LoginPage
    login = LoginPage(page)
    page.goto("https://www.saucedemo.com")
    login.login("standard_user", "secret_sauce")
    return page


@pytest.fixture
def cart_ready_page(logged_in_page):
    """Страница с товаром в корзине"""
    from pages.inventory_page import InventoryPage
    inventory = InventoryPage(logged_in_page)
    inventory.add_backpack()
    inventory.go_to_cart()
    return logged_in_page
