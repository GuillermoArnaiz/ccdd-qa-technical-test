from playwright.sync_api import Page

BASE_URL = "https://alejandromanzanerovsure.pythonanywhere.com"


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = ""):
        self.page.goto(f"{BASE_URL}{path}")
        self.page.wait_for_load_state("domcontentloaded")
