import pytest
from pages.login_page import LoginPage
from playwright.sync_api import expect
from pages.role import AddRolePage
from config.config import LSW


@pytest.mark.parametrize("crm", [LSW])
def test_edit_role(page, crm):
    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])

    roles = AddRolePage(page)
    roles.open_roles()
    roles.edit_role(
        role_name="Automation Test Engineer 2",
        new_name="Updated Automation Test Engineer",
        new_description="Updated description.",
        permissions=[
            {"permission": "Dashboard", "action": "view"},
        ]
    )

    expect(page.get_by_text("Updated Automation Test Engineer")).to_be_visible()