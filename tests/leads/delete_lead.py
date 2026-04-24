import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.leads_page import LeadsPage
from config.config import LSW

@pytest.mark.parametrize("crm", [LSW])
def test_delete_lead(page, crm):

    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])

    page.wait_for_url("**/dashboard", timeout=10000)

    leads = LeadsPage(page)
    leads.open_leads()
    leads.delete_lead("Jane Smith")  # 👈 use first name only in case full name spans columns

    expect(page.locator("table")).not_to_contain_text("John Doe", timeout=10000)
    expect(page.locator(".error-message")).not_to_be_visible()