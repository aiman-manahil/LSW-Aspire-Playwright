import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from config.config import LSW
from pages.tasks_page import TasksPage

@pytest.mark.parametrize("crm", [LSW])
def test_add_task(page, crm):

    page.goto(crm["url"])

    login = LoginPage(page)
    login.login(crm["email"], crm["password"])

    tasks = TasksPage(page)
    tasks.open_tasks()
    tasks.view_task_details("Automated Task")
    expect(page.get_by_role("heading", name="Automated Task")).to_be_visible(timeout=10000)
