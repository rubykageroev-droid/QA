class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.cart_icon = page.locator(".shopping_cart_link")
        self.sort_dropdown = page.locator("[data-test='product_sort_container']")
        self.item_prices = page.locator(".inventory_item_price")
        self.burger_menu = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    def add_backpack(self):
        self.page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()

    def go_to_cart(self):
        self.cart_icon.click()

    def checkout(self):
        self.page.locator("[data-test='checkout']").click()

    def select_sort(self, option: str):
        self.sort_dropdown.wait_for(state="visible")
        self.sort_dropdown.select_option(option)

    def logoutburger(self):
        self.burger_menu.click()
        self.page.wait_for_selector("#logout_sidebar_link", state="visible")
        self.logout_link.click()
