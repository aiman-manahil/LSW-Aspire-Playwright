import pytest
from pages.login_page import LoginPage
from pages.user import UsersPage
from config.config import Aspire


@pytest.mark.parametrize("crm", [Aspire])
def test_add_user(page, crm):
    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])
    users= UsersPage(page)
    users.open_users()
    users.create_user(name="Test Jane Doe",
                    email="test_jane.doe1@example.com",
                    phone="+923364389900",
                    role="Automation Test Engineer 2",
                    password="Password123!",
                    confirm_password="Password123!",
                    status="Active",
                    dob="1990-01-01",
                    join_date="2020-01-01",
                    gender="Male")
    

