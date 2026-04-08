from playwright.sync_api import Page
from .base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = "input[name='username']"
        self.password_input = "input[name='password']"
        self.submit_btn = "button[type='submit']"

    def navigate(self):
        super().navigate("/login/")

    def login(self, username, password):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.submit_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def is_successful(self):
        return "/login/" not in self.page.url

    def get_error(self):
        locator = self.page.locator(".errorlist li, .alert-danger, .invalid-feedback")
        return locator.first.inner_text() if locator.count() > 0 else ""
