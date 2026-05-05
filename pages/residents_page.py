from pages.base_page import BasePage
class ResidentsPage(BasePage):

    def open_residents(self):
        self.page.get_by_role("link", name="Residents").click()
        self.page.wait_for_load_state("networkidle")
    def click_add_resident(self):
        self.page.get_by_role("button", name="Add New Resident").click()
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
    def select_mui_dropdown(self, field_name, value):
        self.page.locator(f"input[name='{field_name}']").locator("xpath=..").locator("div[role='combobox']").click()
        self.page.wait_for_timeout(300)
        self.page.locator(f"li[data-value='{value.lower()}']").click()
        self.page.wait_for_timeout(300)
    def select_mid(self, mid):
        self.page.locator("input[name='moveInDate']").click()
        self.page.locator("input[name='moveInDate']").type(mid)
        self.page.wait_for_timeout(300)

    
    def fill_resident_form(self,legal_name,preferred,gender, unit, room,movein, assigned,status):
        self.page.get_by_placeholder("Legal Name").fill(legal_name)
        self.page.get_by_placeholder("Prefers to be Addressed as").fill(preferred)
        self.select_dropdown("Gender", gender)
        self.page.get_by_placeholder("Unit type").fill(unit)
        self.page.get_by_placeholder("Room No.").fill(room)
        self.select_mid(movein)

        self.select_mui_dropdown("assistedLiving", "False")
        self.select_mui_dropdown("memoryCare", "True")
        self.select_dropdown("Assign To", assigned)
        self.select_dropdown("Status", status)


    
    def save_resident(self):
        self.page.locator("button[type='submit']").click()
        self.page.wait_for_selector("text=Resident Added Successfully", timeout=15000)
    def create_resident(self,  legal_name, preferred,gender, unit, room,movein,assigned, status):
        self.click_add_resident()
        self.fill_resident_form(legal_name, preferred,gender, unit, room,movein,assigned, status)
        self.save_resident()

    #ATTACHMENT
    def upload_attachment(self, file_path):
        file_input = self.page.locator("input[type='file']")
        file_input.set_input_files(file_path)
        self.page.wait_for_timeout(500)
    
    def edit_resident(self,resident_name,name, relationship, address, home_phone, mobile_phone, email, condition, allergies, medications, notes, attachment):
        row = self.page.locator(f"tr:has-text('{resident_name}')")
        # Click 3-dot menu (try multiple locators)
        action_btn = row.locator("[class*='action'], [class*='menu'], [class*='dot'], span, td").last
        action_btn.click()
        self.page.wait_for_timeout(300)
        self.page.get_by_role("button", name="Edit Resident").click()

        self.page.locator("input[name='responsibleParty.name']").fill(name)
        self.page.locator("input[name='responsibleParty.relationship']").fill(relationship)
        self.page.locator("input[name='responsibleParty.address']").fill(address)
        self.page.locator("input[name='responsibleParty.homePhone']").fill(home_phone)
        self.page.locator("input[name='responsibleParty.mobilePhone']").fill(mobile_phone)
        self.page.locator("input[name='responsibleParty.email']").fill(email)
        self.page.locator("input[name='healthDetails.primaryDiagnosisCondition']").scroll_into_view_if_needed()
        self.page.locator("input[name='healthDetails.primaryDiagnosisCondition']").fill(condition)
        self.page.locator("input[name='healthDetails.allergies']").fill(allergies)
        self.page.locator("input[name='healthDetails.medications']").fill(medications)
        self.page.locator("input[name='healthDetails.notes']").fill(notes)
        
        self.upload_attachment(attachment)

        self.page.locator("button[type='submit']").click()
        self.page.wait_for_selector("text=Resident updated successfully!", timeout=15000)

    #DELETE USER
    def delete_resident(self, resident_name):
        row = self.page.locator(f"tr:has-text('{resident_name}')")
        # Click 3-dot menu (try multiple locators)
        action_btn = row.locator("[class*='action'], [class*='menu'], [class*='dot'], span, td").last
        action_btn.click()
        self.page.wait_for_timeout(300)
        self.page.get_by_text("Delete Resident", exact=True).click()
        #confirmation box
        confirm = self.page.get_by_role("button", name="Delete")
        if confirm.is_visible():
            confirm.click()

        self.page.wait_for_selector("text=Resident deleted successfully", timeout=15000)

    #FILTERS
    def filter_by_status(self, status):
        self.page.get_by_role("button", name="Filters").click()
        self.page.wait_for_timeout(300)
        self.page.get_by_text(status, exact=True).click()
        self.page.wait_for_timeout(500)

    #VIEW RESIDENTS DETAILS
    def view_resident_details(self, resident_name):
    # Locate the row (it may not be visible yet)
        row = self.page.locator(f"tr:has-text('{resident_name}')")
    
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