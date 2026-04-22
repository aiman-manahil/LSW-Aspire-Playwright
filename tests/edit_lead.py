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

    # Edit only the name fields
    #leads.edit_lead(
    #   lead_name="John Doe",
    #  first_name="Jane",
    # last_name="Smith",
    #email="jane.smith@example.com",
    # phone="+923004875948",  # keep phone the same
    #)
    leads.add_follow_up(
        lead_name="Jane Smith",
        follow_up_type="Mail",
        key_points="Discussed product features and pricing.",
        next_follow_up_date="2026-04-21",
        next_action="Schedule a demo",
    )

    # Verify change is reflected in the table
    #expect(page.locator("table")).to_contain_text("Jane Smith")
    #expect(page.locator("table")).not_to_contain_text("John Doe")