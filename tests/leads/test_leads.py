import pytest
from pages.login_page import LoginPage
from pages.leads_page import LeadsPage
from config.config import LSW

@pytest.mark.parametrize("crm", [LSW])
def test_create_lead(page, crm):

    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])

    page.wait_for_url("**/dashboard", timeout=10000)

    leads = LeadsPage(page)
    leads.open_leads()
    leads.create_lead(
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        phone="+12345678900",
        assign="Jane Smith",
        lifestyle="Assisted Living",
        looking_for="Myself",
        status="Follow-Up",
        move_in="Immediate",
        lead_source="Referral",
        best_way="Lead automation test - Do not contact",
        message="This is a test lead created by automation. Please do not contact.",
        tags=["VIP", "Referral", "Hot Lead"],  # pass a list

# OR Contacted — pass the date
        contact_status="Contacted",
        contacted_date="2025-01-25",  # YYYY-MM-DD format
    )

    page.wait_for_selector("text=Lead added successfully", timeout=15000)