import pytest
from pages.login_page import LoginPage
from playwright.sync_api import expect
from pages.role import AddRolePage
from config.config import Aspire


@pytest.mark.parametrize("crm", [Aspire])
def test_add_role(page, crm):
    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])

    roles = AddRolePage(page)
    roles.open_roles()
    roles.create_role(
        name="Automation Test Engineer 2",
        description="Manages content and leads.",
        permissions=[
            {"permission": "Facility Management",   "action": "view"},
            {"permission": "Leads Management",     "action": "view"},
            {"permission": "Tasks Management",     "action": "edit"},
            {"permission": "Employee Management",  "action": "view"},
            {"permission": "Reports Management",   "action": "view"},
        ],
        lead_notification=True,
        )
    page.wait_for_timeout(2000)
    expect(page.get_by_text("Automation Test Engineer 2")).to_be_visible()
