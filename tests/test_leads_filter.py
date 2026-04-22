import pytest
from pages.login_page import LoginPage
from pages.leads_page import LeadsPage
from config.config import LSW

@pytest.mark.parametrize("crm", [LSW])

def test_edit_lead(page, crm):
    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])
    page.wait_for_url("**/dashboard", timeout=10000)

    leads = LeadsPage(page)
    leads.open_leads()

    leads.lead_filters(
        lead_status="Follow-Up",
        contact_status="Contacted",
        assigned_user="Katlyn Symon"
    )
    