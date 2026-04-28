
from pages.base_page import BasePage

class UsersPage(BasePage):
    def open_users(self):
        self.page.get_by_role("link", name="Admin & Settings").click()
        self.page.wait_for_load_state("networkidle")
    def click_add_user(self):
        self.page.get_by_role("button", name="Add New User").click()
        self.page.wait_for_timeout(300)
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
    
    def select_dob(self, dob):
        self.page.locator("input[name='dateOfBirth']").fill(dob)
        self.page.wait_for_timeout(300)

    def select_join_date(self, join_date):
        self.page.locator("input[name='joinDate']").fill(join_date)
        self.page.wait_for_timeout(300)
    #FILL PHONE METHOD
    def fill_phone(self, phone_number: str):
        if not phone_number.startswith("+"):
            raise ValueError(f"Phone must start with '+': {phone_number}")

        # Target the visible one specifically
        self.page.locator("div.selected-flag:visible").last.click()
        self.page.wait_for_timeout(300)

        import re
        options = self.page.get_by_role("option").all()

        matched_option = None
        matched_code = ""

        for option in options:
            text = option.inner_text()
            codes = re.findall(r'\+\d+', text)
            if codes:
                code = codes[0]
                if phone_number.startswith(code) and len(code) > len(matched_code):
                    matched_option = option
                    matched_code = code

        if not matched_option:
            raise ValueError(f"No country found in dropdown for: {phone_number}")

        matched_option.click()
        self.page.wait_for_timeout(300)

        local_number = phone_number[len(matched_code):]
        number_input = self.page.locator("input[type='tel']:visible").last
        number_input.click(click_count=3)
        number_input.fill("")
        number_input.type(local_number)

    def fill_user_form(self, name, email, phone, role,password, confirm_password,status,dob,join_date,gender):
        self.page.get_by_placeholder("Full Name").fill(name)
        self.page.get_by_placeholder("Email Address").fill(email)
        self.fill_phone(phone_number=phone)
        self.select_dropdown("Role", role)
        self.page.get_by_placeholder("Enter Password").fill(password)
        self.page.locator("input[name='confirmPassword']").fill(confirm_password)
        self.select_dropdown("Select Status", status)
        self.select_dropdown("Gender",gender)
        self.select_dob(dob)
        self.select_join_date(join_date)

    def save_user(self):
        self.page.locator("button[type='submit']").click()
        self.page.wait_for_selector("text=User and Employee added successfully", timeout=15000)
    def create_user(self, name, email, phone, role,password, confirm_password,status,dob,join_date,gender):
        self.click_add_user()
        self.fill_user_form(name, email, phone, role,password, confirm_password,status,dob,join_date,gender)
        self.save_user()

    #ATTACHMENT
    def upload_attachment(self, file_path):
        file_input = self.page.locator("input[type='file']")
        file_input.set_input_files(file_path)
        self.page.wait_for_timeout(500)

    def edit_user(self, user_name,new_role=None,attachment=None):
        row = self.page.locator(f"tr:has-text('{user_name}')")
        # Click 3-dot menu (try multiple locators)
        action_btn = row.locator("[class*='action'], [class*='menu'], [class*='dot'], span, td").last
        action_btn.click()
        self.page.wait_for_timeout(300)
        self.page.get_by_role("button", name="Edit User").click()
        if new_role:
            self.select_dropdown("Role", new_role)
        if attachment:
            self.upload_attachment(attachment)
        self.page.locator("button[type='submit']").click()
        self.page.wait_for_selector("text=User updated successfully!", timeout=15000)

    #DELETE USER
    def delete_user(self, user_name):
        row = self.page.locator(f"tr:has-text('{user_name}')")
        # Click 3-dot menu (try multiple locators)
        action_btn = row.locator("[class*='action'], [class*='menu'], [class*='dot'], span, td").last
        action_btn.click()
        self.page.wait_for_timeout(300)
        self.page.get_by_text("Delete User", exact=True).click()
        #confirmation box
        confirm = self.page.get_by_role("button", name="Delete")
        if confirm.is_visible():
            confirm.click()

        self.page.wait_for_selector("text=User deleted successfully", timeout=15000)
