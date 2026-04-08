import pytest
from playwright.sync_api import Page
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from utils.data_factory import generate_user, generate_plan


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1280, "height": 720}}


@pytest.fixture
def user_data():
    return generate_user()


@pytest.fixture
def plan_data():
    return generate_plan()


@pytest.fixture
def updated_plan_data():
    return generate_plan(prefix="Updated")


@pytest.fixture
def registered_user(page: Page, user_data):
    r = RegisterPage(page)
    r.navigate()
    r.register(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"],
        confirm_password=user_data["password"],
    )
    return page, user_data


@pytest.fixture
def logged_in_page(page: Page, registered_user):
    p, user_data = registered_user
    login = LoginPage(p)
    login.navigate()
    login.login(username=user_data["username"], password=user_data["password"])
    return p
