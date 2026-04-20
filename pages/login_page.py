from pages.base_page import BasePage

class LoginPage(BasePage):

    def login(self, email, password):
        self.fill("input[type='email']", email)
        self.fill("input[type='password']", password)
        self.page.get_by_label("Remember Me").check()
        self.page.get_by_role("button", name="Sign In").click()