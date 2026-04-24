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
    tasks.task_filters(task_status="Overdue",priority="Normal",assigned_to="Tina Lindsay")
    results = tasks.get_all_task_rows()
    assert len(results) > 0, "No Tasks found"
    for row in results:
        assert row["Status"] == "overdue"
        assert row["Assigned To"] == "Tina Lindsay"
    
