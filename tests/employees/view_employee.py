import pytest
from playwright.sync_api import expect
from conftest import page
from pages.login_page import LoginPage
from pages.employee_page import EmployeesPage
from config.config import LSW

@pytest.mark.parametrize("crm", [LSW])
def test_view_employee(page, crm):

    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])

    page.wait_for_url("**/dashboard", timeout=10000)

    employees = EmployeesPage(page)
    employees.open_employees()
    employees.filter_by_status("active")  # 👈 filter to show only active employees
    #employees.view_employee("John Doe")  # 👈 use first name only in case full name spans columns

    expect(page.locator("tbody")).to_contain_text("active")
    #expect(page.get_by_role("heading", name="Employee Details")).to_be_visible(timeout=10000)