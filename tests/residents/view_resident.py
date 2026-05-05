import pytest
from playwright.sync_api import expect
from conftest import page
from pages.login_page import LoginPage
from pages.residents_page import ResidentsPage
from config.config import LSW

@pytest.mark.parametrize("crm", [LSW])
def test_view_resident(page, crm):

    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])

    page.wait_for_url("**/dashboard", timeout=10000)

    residents= ResidentsPage(page)
    residents.open_residents()
    residents.filter_by_status("occupied")  # 👈 filter to show only active residents
    #residents.view_resident_details("Test Resident")  # 👈 use first name only in case full name spans columns

    expect(page.locator("tbody")).to_contain_text("occupied")
    #expect(page.get_by_role("heading", name="Resident Details")).to_be_visible(timeout=10000)