from pages.base_page import BasePage

class LeadsPage(BasePage):

    def open_leads(self):
        self.page.get_by_role("link", name="Leads").click()
        self.page.wait_for_load_state("networkidle")

    def click_add_lead(self):
        self.page.get_by_role("button", name="Add New Lead").click()


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
    def select_contact_status(self, status, contacted_date=None):
        self.select_dropdown("Contact Status", status)
    
        if status == "Contacted" and contacted_date:
        # Wait for date picker to appear
            self.page.wait_for_selector("input[type='date'], .date-picker, [class*='datepicker']", timeout=3000)
        
        # Try input type date first
        date_input = self.page.locator("input[type='date']")
        if date_input.count() > 0:
            date_input.fill(contacted_date)  # format: "2024-01-25"
        else:
            # Fallback: type into date picker input
            self.page.locator("[class*='datepicker'] input, [class*='date-picker'] input").first.fill(contacted_date)
        
        self.page.wait_for_timeout(300)

    def fill_lead_form(self, first_name, last_name, email, phone, assign, lifestyle, looking_for, status, move_in,lead_source,best_way,contact_status, contacted_date,message):
        self.page.get_by_placeholder("First Name").fill(first_name)
        self.page.get_by_placeholder("Last Name").fill(last_name)
        self.page.wait_for_timeout(300)

        self.page.locator("input[type='email']").fill(email)
        self.page.locator("input[type='tel']").fill(phone)
        self.page.wait_for_timeout(300)
        self.select_contact_status(contact_status, contacted_date)

        self.select_dropdown("Assign To User", assign)
        self.select_dropdown("Select Lifestyle", lifestyle)
        self.select_dropdown("Who You Are Looking For", looking_for)
        self.select_dropdown("Status", status)
        self.select_dropdown("Move In Timeline", move_in)
        self.select_dropdown("Lead Source", lead_source)

        self.page.get_by_placeholder("What's the best way to contact you?").fill(best_way)
        self.page.get_by_placeholder("Add Message").fill(message)

        

    def save_lead(self):
        self.page.locator("button[type='submit']").click()
        self.page.wait_for_selector("text=Lead added successfully", timeout=15000)

    def create_lead(self, first_name, last_name, email, phone, assign, lifestyle, looking_for,status,move_in,lead_source,best_way,contact_status, contacted_date,message):
        self.click_add_lead()
        self.fill_lead_form(first_name, last_name, email, phone, assign, lifestyle, looking_for,status,move_in,lead_source,best_way,contact_status, contacted_date,message)
        self.save_lead()

    def delete_lead(self, lead_name):
    # Find the row containing the lead name
        row = self.page.locator(f"tr:has-text('{lead_name}')")
    
    # Scroll horizontally to the end to reveal action button
        self.page.evaluate("document.querySelector('[class*=\"overflow\"]').scrollLeft += 1000")
        self.page.wait_for_timeout(300)

    # Click the 3-dot menu button in that row
        # Click 3-dot menu (try multiple locators)
        action_btn = row.locator("[class*='action'], [class*='menu'], [class*='dot'], span, td").last
        action_btn.click()
        self.page.wait_for_timeout(300)

    # Click the last option (Delete Lead)
        self.page.get_by_text("Delete lead", exact=True).click()

    # Confirm deletion if a confirmation dialog appears
        confirm = self.page.get_by_role("button", name="Delete")
        if confirm.is_visible():
            confirm.click()

        self.page.evaluate("document.querySelector('[class*=\"overflow\"]').scrollRight += 1000")
