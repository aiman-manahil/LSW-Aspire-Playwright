import pytest
from pages.login_page import LoginPage
from config.config import LSW
from pages.role import AddRolePage

@pytest.mark.parametrize("crm", [LSW])
def test_delete_role(page, crm):

    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])
    roles = AddRolePage(page)
    roles.open_roles()
    roles.delete_role("Automation Test Engineer 1")