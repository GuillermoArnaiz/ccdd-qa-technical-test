import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage


class TestLogin:

    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, page: Page, registered_user):
        _, user_data = registered_user
        login = LoginPage(page)
        login.navigate()
        login.login(username=user_data["username"], password=user_data["password"])
        assert login.is_successful(), f"Login failed, still on {page.url}. Error: {login.get_error()}"

    @pytest.mark.regression
    def test_wrong_password_is_rejected(self, page: Page, registered_user):
        _, user_data = registered_user
        login = LoginPage(page)
        login.navigate()
        login.login(username=user_data["username"], password="thisisnotmypassword")
        assert not login.is_successful(), "Expected login to fail with wrong password"

    @pytest.mark.regression
    def test_unknown_user_is_rejected(self, page: Page):
        login = LoginPage(page)
        login.navigate()
        login.login(username="nobody_at_all_xyz", password="doesntmatter")
        assert not login.is_successful(), "Expected login to fail for unknown user"
