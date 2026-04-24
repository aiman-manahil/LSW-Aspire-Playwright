import pytest
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
    tasks.edit_task(
        task_title="testttt",
        new_description="Updated description for the task.",
        new_category="Updated Category",
        notify_user="Angela Ibarra",
        notify_reason="Transferring task for better expertise."
        )