class CheckoutStepTwo:
    def __init__(self, page):
        self.page = page
        self.finish_button = page.locator("[data-test='finish']")

    def finish(self):
        self.finish_button.click()
