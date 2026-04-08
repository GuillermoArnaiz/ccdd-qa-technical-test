import pytest
from playwright.sync_api import Page
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.data_factory import generate_user, generate_plan


@pytest.mark.smoke
def test_complete_user_journey(page: Page):
    """
    Walks through everything a real user would do in one session:
    register, log in, create a plan, edit it and then delete it.
    """
    user = generate_user()
    plan = generate_plan(prefix="E2E")
    updated = generate_plan(prefix="E2E_v2")

    # step 1 - register
    register = RegisterPage(page)
    register.navigate()
    register.register(
        username=user["username"],
        email=user["email"],
        password=user["password"],
        confirm_password=user["password"],
    )
    assert register.is_successful(), \
        f"Register failed on {page.url}. Errors: {register.get_errors()}"

    # step 2 - log in with the account we just created
    login = LoginPage(page)
    login.navigate()
    login.login(username=user["username"], password=user["password"])
    assert login.is_successful(), \
        f"Login failed on {page.url}. Error: {login.get_error()}"

    dashboard = DashboardPage(page)

    # step 3 - create a plan
    dashboard.create_plan(name=plan["name"], phone1=plan["phone1"], phone2=plan["phone2"])
    assert dashboard.plan_exists(plan["name"]), \
        f"Plan '{plan['name']}' wasn't found after creating it"

    # step 4 - edit it
    dashboard.edit_plan(
        current_name=plan["name"],
        new_name=updated["name"],
        new_phone1=updated["phone1"],
    )
    assert dashboard.plan_exists(updated["name"]), \
        f"Updated plan '{updated['name']}' not visible after editing"
    assert not dashboard.plan_exists(plan["name"]), \
        f"Old name '{plan['name']}' should have disappeared after editing"

    # step 5 - delete it
    dashboard.delete_plan(updated["name"])
    assert not dashboard.plan_exists(updated["name"]), \
        f"Plan '{updated['name']}' is still there after deleting it"
