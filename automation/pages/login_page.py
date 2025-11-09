class LoginPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def login(self, username, password):
        self.driver.get("http://192.168.2.221:3000")  # <-- Replace with actual URL
        self.driver.find_element("id", "username").send_keys(username)
        self.driver.find_element("id", "password").send_keys(password)
        self.driver.find_element("xpath", "/html/body/div/div[1]/div[1]/div/form/div[3]/button").click()
