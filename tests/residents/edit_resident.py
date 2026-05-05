import pytest
from pages.login_page import LoginPage
from pages.residents_page import ResidentsPage
from config.config import LSW

@pytest.mark.parametrize("crm", [LSW])
def test_edit_resident(page, crm):
    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])
    residents = ResidentsPage(page)
    residents.open_residents()
    residents.edit_resident(
        resident_name="Test Resident",
        name="Resident Kin",
        relationship="Sibling",
        address="Main St, Anytown, USA",
        home_phone="555-1234",
        mobile_phone="555-5678",
        email="residentrelation@gmail.com",
        condition="Diabetes",
        allergies="Peanuts",
        medications="Metformin",
        notes="Requires special diet",
        attachment=r"C:\Users\PMYLS\Downloads\leo.jpg"
    )