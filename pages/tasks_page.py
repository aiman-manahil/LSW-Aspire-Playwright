import re

from pages.base_page import BasePage

class TasksPage(BasePage):

    def open_tasks(self):
        self.page.get_by_role("link", name="Tasks").click()
        self.page.wait_for_load_state("networkidle")
    
    def click_add_task(self):
        self.page.get_by_role("button", name="Add New Task").click()

    def select_dropdown(self, label, value):
        dropdown = self.page.locator(f"div:has-text('{label}')").last
        dropdown.click()
        self.page.wait_for_timeout(300)

        option = self.page.get_by_role("option", name=value, exact=True)
        if option.count() > 0:
            option.first.click()
        else:
            input_box = dropdown.locator("input").first
            input_box.fill(value)
            self.page.wait_for_timeout(300)
            self.page.keyboard.press("Enter")
        
        self.page.wait_for_timeout(300)
    
    def select_due_date(self, due_date):
        # Wait for date picker to appear
        self.page.wait_for_selector("input[type='date'], .date-picker, [class*='datepicker']", timeout=3000)
    
        # Try input type date first
        date_input = self.page.locator("input[type='date']")
        if date_input.count() > 0:
            date_input.fill(due_date)  # format: "2026-04-23"
        else:
            # Fallback: type into date picker input
            self.page.locator("[class*='datepicker'] input, [class*='date-picker'] input").first.fill(due_date)
    
        self.page.wait_for_timeout(300)
    
    def fill_task_form(self, title,category,description,assigned_to, due_date,priority,status,comments,attachment):
        self.page.get_by_placeholder("Add Title").fill(title)
        self.page.get_by_placeholder("Add Category").fill(category)
        self.page.get_by_placeholder("Add Description").fill(description)
        # Assigned To has a unique locator
        assigned_dropdown = self.page.locator("div").filter(has_text=re.compile(r"^Assigned To$")).nth(2)
        assigned_dropdown.click()
        self.page.wait_for_timeout(300)
        self.page.get_by_role("option", name=assigned_to, exact=True).first.click()
        self.page.wait_for_timeout(300)

        
        self.select_due_date(due_date)
        self.select_dropdown("Priority", priority)
        self.select_dropdown("Status", status)
        self.page.get_by_placeholder("Add Comments...").fill(comments)
        if attachment:
            self.upload_attachment(attachment)
        
    #ATTACHMENT
    def upload_attachment(self, file_path):
        file_input = self.page.locator("input[type='file']")
        file_input.set_input_files(file_path)
        self.page.wait_for_timeout(500)

    def save_task(self):
        self.page.locator("button[type='submit']").click()
        self.page.wait_for_selector("text=Task added successfully!", timeout=15000)

    def create_task(self, title,category,description,assigned_to, due_date, priority, status, comments,attachment):
        self.click_add_task()
        self.fill_task_form(title,category,description,assigned_to, due_date, priority, status, comments,attachment)
        self.save_task()
    
    def expand_notify_users(self):
        notify_header=self.page.locator("text=Notify Users").first
        notify_header.click()
        self.page.wait_for_timeout(300)

    def notify_user_for_transfer(self, user_name, reason=None):
    # Step 1: Expand the section first
        self.expand_notify_users()
        self.page.wait_for_timeout(300)

    # Step 2: Click using the combobox role inside Notify Users section
        notify_section = self.page.locator("div:has-text('Notify Users')").last
        combobox = notify_section.locator("[role='combobox']").first
        combobox.click()
        self.page.wait_for_timeout(300)

    # Step 3: Type and select
        combobox.fill(user_name)
        self.page.wait_for_timeout(300)

        option = self.page.get_by_role("option", name=user_name, exact=True)
        if option.count() > 0:
            option.first.click()
        else:
            self.page.keyboard.press("Enter")

        self.page.wait_for_timeout(300)

    # Step 4: Fill reason
        if reason:
            self.page.get_by_placeholder("Explain why you're transferring this task...").fill(reason)

    def edit_task(self, task_title,new_description=None,new_category=None,notify_user=None,notify_reason=None):
        # Click the row directly to open the edit form
        row = self.page.locator(f"tr:has-text('{task_title}')")
        row.click()
        self.page.wait_for_timeout(500)

        if new_description:
            self.page.get_by_placeholder("Add Description").clear()
            self.page.get_by_placeholder("Add Description").fill(new_description)

        if new_category:
            self.page.get_by_placeholder("Add Category").clear()
            self.page.get_by_placeholder("Add Category").fill(new_category)
        
        if notify_user:
            self.notify_user_for_transfer(notify_user, notify_reason)

        self.page.locator("button[type='submit']").click()
        self.page.wait_for_selector("text=Task updated and notification sent successfully!", timeout=15000)
        
    #DELETE TASK
    def delete_task(self, task_title):
        row = self.page.locator(f"tr:has-text('{task_title}')")
        # Click 3-dot menu (try multiple locators)
        action_btn = row.locator("[class*='action'], [class*='menu'], [class*='dot'], span, td").last
        action_btn.click()
        self.page.wait_for_timeout(300)
        self.page.get_by_text("Delete Task", exact=True).click()
        #confirmation box
        confirm = self.page.get_by_role("button", name="Delete")
        if confirm.is_visible():
            confirm.click()

        self.page.wait_for_selector("text=Task deleted successfully", timeout=15000)
    #VIEW DETAILS
    def view_task_details(self, task_title):
        row = self.page.locator(f"tr:has-text('{task_title}')")
        # Click 3-dot menu (try multiple locators)
        action_btn = row.locator("[class*='action'], [class*='menu'], [class*='dot'], span, td").last
        action_btn.click()
        self.page.wait_for_timeout(300)
        self.page.get_by_text("View Details", exact=True).click()

    #FILTERSSSSS
    def click_filter_button(self):
        self.page.get_by_role("button", name="Filters").click()
    def apply_filter(self):
        self.page.get_by_role("button", name="Apply Filter").click()
        self.page.wait_for_timeout(500)
    def task_filters(self, task_status,priority,assigned_to):
        self.click_filter_button()
        self.select_dropdown("Task Status", task_status)
        self.select_dropdown("Priority", priority)
        self.select_dropdown("Assigned To", assigned_to)
        self.apply_filter()

    def get_all_task_rows(self):
        self.page.wait_for_selector("table tbody tr", timeout=10000)
        self.page.wait_for_timeout(500)
        rows = self.page.locator("table tbody tr")
        print(f"Total rows found: {rows.count()}")
        if rows.count() > 0:
            print(rows.nth(0).inner_html())
        data = []

        for i in range(rows.count()):
            row = rows.nth(i)
            cells =row.locator("td")
            data.append({
                "Status": cells.nth(5).inner_text().strip(),     # adjust index
                "Assigned To": cells.nth(2).inner_text().strip() # adjust index
                })
        return data
