import pytest
from pages.login_page import LoginPage
from playwright.sync_api import expect
from pages.user import UsersPage
from config.config import LSW


@pytest.mark.parametrize("crm", [LSW])
def test_edit_user(page, crm):
    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])
    users= UsersPage(page)
    users.open_users()
    users.edit_user(
        user_name="Jane Smith",
        new_role="Automation Test Engineer",
        attachment=r"C:\Users\PMYLS\Downloads\celina.jpg"
    )