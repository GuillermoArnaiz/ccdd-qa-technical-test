import pytest
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage


class TestCreatePlan:

    @pytest.mark.smoke
    def test_create_plan_shows_up_on_dashboard(self, logged_in_page: Page, plan_data):
        dashboard = DashboardPage(logged_in_page)
        dashboard.create_plan(name=plan_data["name"], phone1=plan_data["phone1"])
        assert dashboard.plan_exists(plan_data["name"]), \
            f"Created '{plan_data['name']}' but it didn't appear on the dashboard"

    @pytest.mark.regression
    def test_create_plan_with_two_phones(self, logged_in_page: Page, plan_data):
        dashboard = DashboardPage(logged_in_page)
        dashboard.create_plan(
            name=plan_data["name"],
            phone1=plan_data["phone1"],
            phone2=plan_data["phone2"],
        )
        assert dashboard.plan_exists(plan_data["name"]), \
            f"Created '{plan_data['name']}' with two phones but it didn't appear on the dashboard"


class TestEditPlan:

    @pytest.mark.smoke
    def test_edit_plan_updates_name(self, logged_in_page: Page, plan_data, updated_plan_data):
        dashboard = DashboardPage(logged_in_page)

        dashboard.create_plan(name=plan_data["name"], phone1=plan_data["phone1"])
        assert dashboard.plan_exists(plan_data["name"]), "Precondition: plan should exist before editing"

        dashboard.edit_plan(
            current_name=plan_data["name"],
            new_name=updated_plan_data["name"],
            new_phone1=updated_plan_data["phone1"],
        )

        assert dashboard.plan_exists(updated_plan_data["name"]), \
            f"After edit, expected '{updated_plan_data['name']}' to be visible"
        assert not dashboard.plan_exists(plan_data["name"]), \
            f"After edit, old name '{plan_data['name']}' should be gone"


class TestDeletePlan:

    @pytest.mark.smoke
    def test_delete_plan_removes_it(self, logged_in_page: Page, plan_data):
        dashboard = DashboardPage(logged_in_page)

        dashboard.create_plan(name=plan_data["name"], phone1=plan_data["phone1"])
        assert dashboard.plan_exists(plan_data["name"]), "Precondition: plan should exist before deleting"

        dashboard.delete_plan(plan_data["name"])

        assert not dashboard.plan_exists(plan_data["name"]), \
            f"Deleted '{plan_data['name']}' but it's still showing on the dashboard"
