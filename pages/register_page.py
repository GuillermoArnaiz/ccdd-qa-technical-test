from playwright.sync_api import Page
from .base_page import BasePage


class RegisterPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = "input[name='username']"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.confirm_input = "input[name='password_confirm']"
        self.submit_btn = "button[type='submit']"

    def navigate(self):
        super().navigate("/register/")

    def register(self, username, email, password, confirm_password):
        self.page.fill(self.username_input, username)
        self.page.fill(self.email_input, email)
        self.page.fill(self.password_input, password)
        self.page.fill(self.confirm_input, confirm_password)
        self.page.click(self.submit_btn)
        self.page.wait_for_load_state("domcontentloaded")

    def is_successful(self):
        # after a successful registration django redirects away from /register/
        return "/register/" not in self.page.url

    def get_errors(self):
        locator = self.page.locator(".errorlist li, .alert-danger, .invalid-feedback")
        return [locator.nth(i).inner_text() for i in range(locator.count())]
