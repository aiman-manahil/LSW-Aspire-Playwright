import pytest
from pages.login_page import LoginPage
from pages.residents_page import ResidentsPage
from config.config import LSW

@pytest.mark.parametrize("crm", [LSW])
def test_add_resident(page, crm):
    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])
    residents = ResidentsPage(page)
    residents.open_residents()
    residents.create_resident(
    legal_name="Test Resident",
    preferred="TR",
    gender="Male",
    unit="Apartment",
    room="102",
    movein="05/10/2026",
    status="Occupied",
    assigned="John Doe"
)