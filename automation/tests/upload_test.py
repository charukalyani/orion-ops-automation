from automation.pages.login_page import LoginPage
from automation.pages.dashboard_page import DashboardPage
from automation.pages.upload_page import UploadPage
from automation.utils.excel_logger import ExcelLogger
from automation.utils.browser_setup import get_driver as start_browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

BASE_URL = "http://192.168.2.221:3000"
CREDENTIALS = {"username": "admin", "password": "admin@123"}
TEST_FILE = os.path.abspath("sample_upload.txt")  # prepare your file in same directory

# Ensure sample file exists
if not os.path.exists(TEST_FILE):
    with open(TEST_FILE, "w") as f:
        f.write("Test file upload by automation.\n")

def run_upload_test():
    driver = None
    log = ExcelLogger()
    try:
        driver = start_browser()
        wait = WebDriverWait(driver, 10)
        login_page = LoginPage(driver, wait)
        dash = DashboardPage(driver, wait)
        upload = UploadPage(driver, wait)

        # Step 1: Login
        driver.get(BASE_URL)
        login_page.login(CREDENTIALS["username"], CREDENTIALS["password"])
        wait.until(EC.url_contains("/dashboard"))

        # Step 2: Navigate to Upload page
        dash.nav_to("Upload")
        wait.until(EC.url_contains("/upload"))

        # Step 3: Upload file
        print("[Test] Uploading file:", TEST_FILE)
        result = upload.upload_file(TEST_FILE)

        # Step 4: Log result
        if result:
            log.log("UPLOAD", "TC_UPLOAD_01", "Verify File Upload Functionality", "PASS")
        else:
            log.log("UPLOAD", "TC_UPLOAD_01", "Verify File Upload Functionality", "FAIL", "Upload failed or message not shown")

    except Exception as e:
        log.log("UPLOAD", "TC_UPLOAD_01", "Verify File Upload Functionality", "FAIL", str(e))
        print("Test failed:", e)
    finally:
        if driver:
            driver.quit()
            print("Browser closed.")

if __name__ == "__main__":
    run_upload_test()
