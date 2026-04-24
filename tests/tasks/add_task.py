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
    tasks.create_task(title="Automated Task",
                    description="This task was created by an automated test.", 
                    due_date="2026-04-24",
                    category="General",
                    assigned_to="Angela Ibarra",
                    priority="Normal",
                    status="In Progress",
                    comments="This is an automated task.",
                    attachment=r"C:\Users\PMYLS\Downloads\salons_list.pdf"
                    )
    