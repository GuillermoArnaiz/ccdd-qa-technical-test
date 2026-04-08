from playwright.sync_api import Page
from .base_page import BasePage

BASE_URL = "https://alejandromanzanerovsure.pythonanywhere.com"


class DashboardPage(BasePage):
    """
    Handles everything on the main screen: creating, editing and deleting plans.

    One thing worth noting: the app has a bug where the create/edit forms
    render two csrfmiddlewaretoken fields with different values. Django sees
    that mismatch, rejects the POST and redirects to /logout/. To get around
    it I submit those forms via fetch() from inside the browser — that way
    the live session cookies are used directly and the CSRF check passes.

    The delete button uses a native browser confirm() dialog, so I register
    a one-time dialog handler before clicking to accept it automatically.
    """

    def __init__(self, page: Page):
        super().__init__(page)

    def navigate(self):
        super().navigate("/")

    def _get_csrf(self):
        cookies = self.page.context.cookies()
        return next(c["value"] for c in cookies if c["name"] == "csrftoken")

    def _submit_via_fetch(self, path, fields):
        csrf = self._get_csrf()
        fd_lines = "\n".join(f"  fd.append({k!r}, {v!r});" for k, v in fields.items())
        self.page.evaluate(f"""async () => {{
            const fd = new FormData();
            fd.append('csrfmiddlewaretoken', '{csrf}');
{fd_lines}
            await fetch('{path}', {{
                method: 'POST',
                body: fd,
                credentials: 'include',
                redirect: 'manual'
            }});
        }}""")
        self.page.goto(f"{BASE_URL}/")
        self.page.wait_for_load_state("domcontentloaded")

    def _edit_link_for(self, plan_name):
        card = self.page.locator(".action-plan-card", has=self.page.locator(f"text={plan_name}")).first
        return card.locator("a[href*='/edit/']").get_attribute("href")

    def _card_for(self, plan_name):
        return self.page.locator(".action-plan-card", has=self.page.locator(f"text={plan_name}")).first

    # -- actions ---------------------------------------------------------------

    def create_plan(self, name, phone1, phone2="", phone3=""):
        fields = {"action_plan_name": name, "phone_1": phone1}
        if phone2:
            fields["phone_2"] = phone2
        if phone3:
            fields["phone_3"] = phone3
        self._submit_via_fetch("/create/", fields)

    def edit_plan(self, current_name, new_name, new_phone1, new_phone2=""):
        href = self._edit_link_for(current_name)
        fields = {"action_plan_name": new_name, "phone_1": new_phone1}
        if new_phone2:
            fields["phone_2"] = new_phone2
        self._submit_via_fetch(href, fields)

    def delete_plan(self, name):
        self.page.goto(f"{BASE_URL}/")
        self.page.wait_for_load_state("domcontentloaded")
        self.page.once("dialog", lambda d: d.accept())
        self._card_for(name).locator("button:has-text('Eliminar')").click()
        self.page.wait_for_load_state("domcontentloaded")

    def plan_exists(self, name):
        return self._card_for(name).count() > 0

    def logout(self):
        self.page.locator("button:has-text('Cerrar Sesión')").click()
        self.page.wait_for_load_state("domcontentloaded")
