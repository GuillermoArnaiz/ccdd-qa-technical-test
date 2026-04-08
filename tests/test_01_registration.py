import pytest
from playwright.sync_api import Page
from pages.register_page import RegisterPage


class TestRegistration:

    @pytest.mark.smoke
    def test_register_new_user(self, page: Page, user_data):
        r = RegisterPage(page)
        r.navigate()
        r.register(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            confirm_password=user_data["password"],
        )
        assert r.is_successful(), f"Registration failed, still on {page.url}. Errors: {r.get_errors()}"

    @pytest.mark.regression
    def test_cant_register_same_username_twice(self, page: Page, registered_user):
        _, user_data = registered_user
        r = RegisterPage(page)
        r.navigate()
        r.register(
            username=user_data["username"],
            email="another@example.com",
            password=user_data["password"],
            confirm_password=user_data["password"],
        )
        assert not r.is_successful(), "Expected an error for duplicate username, but registration went through"

    @pytest.mark.regression
    def test_passwords_must_match(self, page: Page, user_data):
        r = RegisterPage(page)
        r.navigate()
        r.register(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            confirm_password="something_completely_different",
        )
        assert not r.is_successful(), "Expected an error for mismatched passwords, but registration went through"
