class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, url):
        self.page.goto(url)

    def click(self, selector):
        self.page.click(selector)

    def fill(self, selector, text):
        self.page.fill(selector, text)