import pytest
from pages.login_page import LoginPage
from pages.employee_page import EmployeesPage
from config.config import LSW


@pytest.mark.parametrize("crm", [LSW])
def test_add_employee(page, crm):
    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])
    employees = EmployeesPage(page)
    employees.open_employees()
    employees.create_employee(name="Deleted employee 1",
                    email="deleted.employee1@example.com",
                    phone="+917387128783",
                    role="Automation Test Engineer",
                    dob="1990-01-01",
                    join_date="2020-01-01",
                    gender="Male",
                    attachment=r"C:\Users\PMYLS\Downloads\celina.jpg")
    
    

