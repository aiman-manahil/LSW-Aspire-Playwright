

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
    
    def fill_tags(self, tags: list):
        tag_input = self.page.get_by_placeholder("Enter tag name and press Enter or click Add")
    
        for tag in tags:
            tag_input.fill(tag)
            tag_input.press("Enter")
            self.page.wait_for_timeout(300)  # small wait between tags
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

    def fill_lead_form(self, first_name, last_name, email, phone, assign, lifestyle, looking_for, status, move_in,lead_source,best_way,contact_status, contacted_date,message, tags=None):
        self.page.get_by_placeholder("First Name").fill(first_name)
        self.page.get_by_placeholder("Last Name").fill(last_name)
        self.page.wait_for_timeout(300)

        self.page.locator("input[type='email']").fill(email)
        self.fill_phone(phone_number=phone)  # no country argument needed at all
        self.select_contact_status(contact_status, contacted_date)

        self.select_dropdown("Assign To User", assign)
        self.select_dropdown("Select Lifestyle", lifestyle)
        self.select_dropdown("Who You Are Looking For", looking_for)
        self.select_dropdown("Status", status)
        self.select_dropdown("Move In Timeline", move_in)
        self.select_dropdown("Lead Source", lead_source)

        self.page.get_by_placeholder("What's the best way to contact you?").fill(best_way)
        self.page.get_by_placeholder("Add Message").fill(message)
        if tags:
            self.fill_tags(tags)


    def save_lead(self):
        self.page.locator("button[type='submit']").click()
        self.page.wait_for_selector("text=Lead added successfully", timeout=15000)

    def create_lead(self, first_name, last_name, email, phone, assign, lifestyle, looking_for,status,move_in,lead_source,best_way,contact_status, contacted_date,message,tags=None):
        self.click_add_lead()
        self.fill_lead_form(first_name, last_name, email, phone, assign, lifestyle, looking_for,status,move_in,lead_source,best_way,contact_status, contacted_date,message, tags=tags)
        self.save_lead()
    
    
    #DELETE LEAD METHOD
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

    #EDIT LEAD METHOD
    def edit_lead(self, lead_name, first_name=None, last_name=None, email=None, phone=None):
    # Click the row directly to open the edit form
        row = self.page.locator(f"tr:has-text('{lead_name}')")
        row.click()
        self.page.wait_for_timeout(500)

    # Fill only the fields that are passed
        if first_name:
            self.page.get_by_placeholder("First Name").clear()
            self.page.get_by_placeholder("First Name").fill(first_name)

        if last_name:
            self.page.get_by_placeholder("Last Name").clear()
            self.page.get_by_placeholder("Last Name").fill(last_name)

        if email:
            self.page.locator("input[type='email']").clear()
            self.page.locator("input[type='email']").fill(email)

        if phone:
            self.page.wait_for_selector("div.selected-flag", timeout=5000)  # wait for phone field to load
            self.fill_phone(phone_number=phone)
    # Save
        self.page.locator("button[type='submit']").click()
        self.page.wait_for_selector("text=Lead updated successfully", timeout=15000)
    
    def add_follow_up(self, follow_up_type=None, key_points=None, next_follow_up_date=None, next_action=None, lead_name=None):
    # If lead_name is provided, open the lead first

        if lead_name:
            row = self.page.locator(f"tr:has-text('{lead_name}')")
            row.locator("td").nth(1).click()
            self.page.wait_for_timeout(500)
            

    # Click the + Add Follow-Up button
        self.page.get_by_role("button", name="Add Follow-Up").click()
        self.page.screenshot(path="after_followup_btn.png")
        self.page.wait_for_selector("text=Add Follow-Up", timeout=5000)

    # Select follow-up type if provided
        if follow_up_type:
            self.page.get_by_role("button", name=follow_up_type, exact=True).click()

    # Fill key points / questions
        if key_points:
            self.page.get_by_placeholder("Record details of the conversation...").fill(key_points)

    # Fill next follow-up date (expects "YYYY-MM-DD" format)
        if next_follow_up_date:
            self.page.locator("input[type='date']").fill(next_follow_up_date)

    # Fill next action
        if next_action:
            self.page.get_by_placeholder("e.g. Call again").fill(next_action)

    # Save
        self.page.get_by_role("button", name="Save Note").click()
        self.page.wait_for_selector("text=Follow-up note added!", timeout=15000)

# Click Update Lead to save the form
        self.page.locator("button[type='submit']").click()
        self.page.wait_for_selector("text=Lead updated successfully!", timeout=15000)

    def click_filter_button(self):
        self.page.get_by_role("button", name="Filters").click()
    def apply_filter(self):
        self.page.get_by_role("button", name="Apply Filter").click()
        self.page.wait_for_timeout(500)
    def lead_filters(self, lead_status,contact_status, assigned_user):
    # Open filter modal
        self.click_filter_button()
        self.select_dropdown("Assigned User", assigned_user)
        self.select_dropdown("Contact Status", contact_status)
        self.select_dropdown("Lead Status", lead_status)
        self.apply_filter()
    def clean(self, text):
        import re
        text = text.replace('\u200b', '').replace('\n', '').strip()
        text = re.sub(r'\s*\(.*?\)', '', text)  # removes (07-Apr-2026)
        return text.strip()

    def get_all_lead_rows(self):
        self.page.wait_for_selector("table tbody tr", timeout=10000)
        self.page.wait_for_timeout(500)
        rows = self.page.locator("table tbody tr")
        data = []

        for i in range(rows.count()):
            row = rows.nth(i)
            cells=row.locator("td")
            data.append({
                "Assigned User": self.clean(cells.nth(4).inner_text()),
                "Status": self.clean(cells.nth(5).inner_text()),
                "Contact Status": self.clean(cells.nth(6).inner_text())
                })
        return data

    def view_lead(self, lead_name):
    # Locate the row (it may not be visible yet)
        row = self.page.locator(f"tr:has-text('{lead_name}')")
    
    # Scroll the row into view first (vertical scroll)
        row.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        # Scroll horizontally to the end to reveal action button
        self.page.evaluate("document.querySelector('[class*=\"overflow\"]').scrollLeft += 1000")
        self.page.wait_for_timeout(300)

    # Click the 3-dot menu button in that row
        # Click 3-dot menu (try multiple locators)
        action_btn = row.locator("[class*='action'], [class*='menu'], [class*='dot'], span, td").last
        action_btn.click()
        self.page.wait_for_timeout(300)

    # Click the last option (View Details)
        self.page.get_by_text("View Details", exact=True).click()

    def aspire_view_leads(self, lead_name):
        # Click the row directly to open the edit form
        row = self.page.locator(f"tr:has-text('{lead_name}')")
        row.click()
        self.page.wait_for_timeout(500)