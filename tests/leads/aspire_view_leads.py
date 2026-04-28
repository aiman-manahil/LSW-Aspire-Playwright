import pytest
from playwright.sync_api import expect
from conftest import page
from pages.login_page import LoginPage
from pages.leads_page import LeadsPage
from config.config import Aspire

@pytest.mark.parametrize("crm", [Aspire])
def test_delete_lead(page, crm):

    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])

    page.wait_for_url("**/dashboard", timeout=10000)

    leads = LeadsPage(page)
    leads.open_leads()
    leads.view_lead("John Doe")  # 👈 use first name only in case full name spans columns


    expect(page.get_by_role("heading", name="John Doe")).to_be_visible(timeout=10000)