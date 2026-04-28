from pages.base_page import BasePage


class AddRolePage(BasePage):

    def open_roles(self):
        self.page.get_by_role("link", name="Admin & Settings").click()
        self.page.wait_for_load_state("networkidle")

    def click_add_role(self):
        self.page.get_by_role("button", name="Add New Role").click()
        self.page.wait_for_timeout(300)

    def fill_role_name(self, name):
        self.page.get_by_placeholder("Role Name").fill(name)

    def fill_role_description(self, description):
        self.page.get_by_placeholder("Role Description").fill(description)

    def set_permission(self, permission, action):
        """Check a permission checkbox by row name and action (view/add/edit/delete)."""
        col_index = ["view", "add", "edit", "delete"].index(action.lower())
        row = self.page.locator("tr").filter(has_text=permission)
        row.locator("input[type='checkbox']").nth(col_index).check()
        self.page.wait_for_timeout(200)

    def toggle_lead_notification(self):
        self.page.locator("button[role='switch'], input[type='checkbox']").last.click()
        self.page.wait_for_timeout(200)

    def save_role(self):
        self.page.get_by_role("button", name="Add Role").click()
        self.page.wait_for_timeout(1000)

    def cancel(self):
        self.page.get_by_role("button", name="Cancel").click()
        self.page.wait_for_timeout(300)

    def create_role(self, name, description=None, permissions=None, lead_notification=False):
        self.click_add_role()
        self.fill_role_name(name)
        if description:
            self.fill_role_description(description)
        if permissions:
            for p in permissions:
                self.set_permission(p["permission"], p["action"])
        if lead_notification:
            self.toggle_lead_notification()
        self.save_role()

    def edit_role(self, role_name, new_name=None, new_description=None, permissions=None):
        row = self.page.locator(f"tr:has-text('{role_name}')")
        # Click 3-dot menu (try multiple locators)
        action_btn = row.locator("[class*='action'], [class*='menu'], [class*='dot'], span, td").last
        action_btn.click()
        self.page.wait_for_timeout(300)
        self.page.get_by_text("Edit Role", exact=True).click()
        if new_name:
            self.page.locator("input[name='roleName']").clear()
            self.page.locator("input[name='roleName']").fill(new_name)

        if new_description:
            self.page.locator("input[name='roleDescription']").clear()
            self.page.locator("input[name='roleDescription']").fill(new_description)


        if permissions:
            for p in permissions:
                self.set_permission(p["permission"], p["action"])

        self.page.get_by_role("button", name="Update Role").click()
        self.page.wait_for_timeout(1000)

    #DELETE ROLE
    def delete_role(self, role_name):
        row = self.page.locator(f"tr:has-text('{role_name}')")
        # Click 3-dot menu (try multiple locators)
        action_btn = row.locator("[class*='action'], [class*='menu'], [class*='dot'], span, td").last
        action_btn.click()
        self.page.wait_for_timeout(300)
        self.page.get_by_text("Delete Role", exact=True).click()
        #confirmation box
        confirm = self.page.get_by_role("button", name="Delete")
        if confirm.is_visible():
            confirm.click()

        self.page.wait_for_selector("text=Role deleted successfully", timeout=15000)