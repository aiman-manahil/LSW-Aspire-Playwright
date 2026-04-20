import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from config.config import LSW, Aspire

@pytest.mark.parametrize("crm", [LSW, Aspire])
def test_login(page, crm):

    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])

    page.wait_for_load_state("networkidle")
    expect(page.locator("text=Logout")).to_be_visible()

    # dashboard checks
    page.wait_for_url("**/dashboard")
    expect(page.get_by_text("Organization Dashboard")).to_be_visible()

