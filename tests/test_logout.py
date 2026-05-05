import pytest
from pages.login_page import LoginPage
from playwright.sync_api import expect
from config.config import LSW


@pytest.mark.parametrize("crm", [LSW])
def test_logout(page, crm):
    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])

    page.get_by_role("link", name="Logout").click()
    
    expect(page.get_by_role("button", name="Sign In")).to_be_visible()