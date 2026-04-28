import pytest
from pages.login_page import LoginPage
from playwright.sync_api import expect
from config.config import LSW
from pages.user import UsersPage

@pytest.mark.parametrize("crm", [LSW])
def test_delete_user(page, crm):

    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])
    users = UsersPage(page)
    users.open_users()
    users.delete_user("Jane Doe")
