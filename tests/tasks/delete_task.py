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
    tasks.delete_task("testttt")
    expect(page.locator("table")).not_to_contain_text("testttt", timeout=10000)
    expect(page.locator(".error-message")).not_to_be_visible()