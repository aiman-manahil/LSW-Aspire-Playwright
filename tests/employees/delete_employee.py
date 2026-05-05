import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.employee_page import EmployeesPage
from config.config import LSW

@pytest.mark.parametrize("crm", [LSW])
def test_delete_employee(page, crm):

    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])

    page.wait_for_url("**/dashboard", timeout=10000)

    employee=EmployeesPage(page)
    employee.open_employees()
    employee.delete_employee("erhfb")  # 👈 use first name only in case full
    
    expect(page.locator(".error-message")).not_to_be_visible()