import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.residents_page import ResidentsPage
from config.config import LSW

@pytest.mark.parametrize("crm", [LSW])
def test_delete_resident(page, crm):

    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])

    page.wait_for_url("**/dashboard", timeout=10000)

    resident=ResidentsPage(page)
    resident.open_residents()
    resident.delete_resident("Test Resident")  # 👈 use first name only in case full
    
    expect(page.locator(".error-message")).not_to_be_visible()