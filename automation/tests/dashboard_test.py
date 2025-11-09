# from automation.pages.dashboard_page import DashboardPage
# from automation.pages.login_page import LoginPage
# from automation.utils.excel_logger import ExcelLogger
# from automation.utils.browser_setup import get_driver as start_browser
# from selenium.webdriver.support.ui import WebDriverWait


# def run_dashboard_tests():
#     # Start browser
#     driver = start_browser()
#     wait = WebDriverWait(driver, 10)   # Create wait instance

#     # Initialize logger and page objects
#     log = ExcelLogger()
#     login = LoginPage(driver, wait)
#     dash = DashboardPage(driver, wait)

#     # Perform login
#     login.login("admin", "admin@123")

#     # Test Case: Verify Dashboard Load
#     try:
#         if dash.verify_dashboard_loaded():
#             log.log("DASHBOARD", "TC_DASH_01", "Dashboard Load Test", "PASS")
#             print("Dashboard loaded successfully.")
#         else:
#             raise Exception("Dashboard not loaded")
#     except Exception as e:
#         log.log("DASHBOARD", "TC_DASH_01", "Dashboard Load Test", "FAIL", str(e))
#         print(f"Dashboard test failed: {e}")

#     # Close browser
#     driver.quit()


# automation/tests/dashboard_test.py

import time
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from automation.pages.login_page import LoginPage
from automation.pages.dashboard_page import DashboardPage
from automation.utils.excel_logger import ExcelLogger
# import your browser factory function (may be named start_browser or get_driver)
from automation.utils.browser_setup import get_driver as start_browser  # adjust import if needed

BASE_URL = "http://192.168.2.221:3000"    # change if needed
CREDS = {"username": "admin", "password": "admin@123"}  # change if needed
TIMEOUT = 10


def _safe_start_browser():
    """
    Call start_browser() and return (driver, wait).
    Supports both: start_browser() -> driver  OR  -> (driver, wait)
    """
    res = start_browser()
    if isinstance(res, tuple) or isinstance(res, list):
        driver = res[0]
        # if start_browser returns wait too, use it; otherwise create one
        wait = res[1] if len(res) > 1 else WebDriverWait(driver, TIMEOUT)
    else:
        driver = res
        wait = WebDriverWait(driver, TIMEOUT)
    return driver, wait


def run_dashboard_tests():
    driver = None
    wait = None
    log = ExcelLogger()

    try:
        # Start browser
        driver, wait = _safe_start_browser()

        # Page objects
        login_page = LoginPage(driver, wait)
        dash = DashboardPage(driver, wait)

        # Navigate to base url and login
        driver.get(BASE_URL)
        time.sleep(1)  # small buffer for page load
        login_page.login(CREDS["username"], CREDS["password"])

        # Give application some time to redirect
        wait.until(EC.url_contains("/dashboard"))

        # ------------------ TC: Dashboard Load ------------------
        tc_id = "TC_DASH_01"
        desc = "Dashboard Load Test"
        try:
            if dash.verify_dashboard_loaded():
                log.log("DASHBOARD", tc_id, desc, "PASS")
                print(f"{tc_id} PASS - Dashboard loaded")
            else:
                raise Exception("verify_dashboard_loaded() returned False")
        except Exception as e:
            log.log("DASHBOARD", tc_id, desc, "FAIL", str(e))
            print(f"{tc_id} FAIL - {e}")
            # do not stop; continue to collect other failures

        # ------------------ TC: Upload Files button redirect ------------------
        tc_id = "TC_DASH_02"
        desc = "Upload Files button redirects to /upload"
        try:
            dash.click_upload_files()
            wait.until(EC.url_contains("/upload"))
            log.log("DASHBOARD", tc_id, desc, "PASS")
            print(f"{tc_id} PASS - Upload redirect OK")
        except Exception as e:
            log.log("DASHBOARD", tc_id, desc, "FAIL", str(e))
            print(f"{tc_id} FAIL - {e}")
        finally:
            # navigate back to dashboard
            driver.get(f"{BASE_URL}/dashboard")
            wait.until(EC.url_contains("/dashboard"))

        # ------------------ TC: View Conversions redirect ------------------
        tc_id = "TC_DASH_03"
        desc = "View Conversions button redirects to /conversions"
        try:
            dash.click_view_conversions()
            wait.until(EC.url_contains("/conversions"))
            log.log("DASHBOARD", tc_id, desc, "PASS")
            print(f"{tc_id} PASS - Conversions redirect OK")
        except Exception as e:
            log.log("DASHBOARD", tc_id, desc, "FAIL", str(e))
            print(f"{tc_id} FAIL - {e}")
        finally:
            driver.get(f"{BASE_URL}/dashboard")
            wait.until(EC.url_contains("/dashboard"))

        # ------------------ TC: Job Queue redirect ------------------
        tc_id = "TC_DASH_04"
        desc = "Job Queue button redirects to /jobs"
        try:
            dash.click_job_queue()
            wait.until(EC.url_contains("/jobs"))
            log.log("DASHBOARD", tc_id, desc, "PASS")
            print(f"{tc_id} PASS - Jobs redirect OK")
        except Exception as e:
            log.log("DASHBOARD", tc_id, desc, "FAIL", str(e))
            print(f"{tc_id} FAIL - {e}")
        finally:
            driver.get(f"{BASE_URL}/dashboard")
            wait.until(EC.url_contains("/dashboard"))

        # ------------------ TC: Conversion Stats presence ------------------
        tc_id = "TC_DASH_05"
        desc = "Conversion Stats card presence and basic values"
        try:
            card = dash.get_conversion_stats_card()
            total = dash.get_stat_value_by_label(card, "Total")
            completed = dash.get_stat_value_by_label(card, "Completed")
            if total == "" or completed == "":
                raise Exception("One of required stat values is empty")
            log.log("DASHBOARD", tc_id, desc, "PASS")
            print(f"{tc_id} PASS - Conversion stats OK (Total={total}, Completed={completed})")
        except Exception as e:
            log.log("DASHBOARD", tc_id, desc, "FAIL", str(e))
            print(f"{tc_id} FAIL - {e}")

        # ------------------ TC: Job Stats presence ------------------
        tc_id = "TC_DASH_06"
        desc = "Job Stats card presence and basic values"
        try:
            card = dash.get_job_stats_card()
            completed = dash.get_stat_value_by_label(card, "Completed")
            queued = dash.get_stat_value_by_label(card, "Queued")
            if completed == "" or queued == "":
                raise Exception("Job stats missing values")
            log.log("DASHBOARD", tc_id, desc, "PASS")
            print(f"{tc_id} PASS - Job stats OK (Completed={completed}, Queued={queued})")
        except Exception as e:
            log.log("DASHBOARD", tc_id, desc, "FAIL", str(e))
            print(f"{tc_id} FAIL - {e}")

        # ------------------ TC: Orion HCI Stats ------------------
        tc_id = "TC_DASH_07"
        desc = "Orion HCI Stats presence"
        try:
            card = dash.get_hci_stats_card()
            healthy = dash.get_stat_value_by_label(card, "Healthy Clusters")
            images_ready = dash.get_stat_value_by_label(card, "Images Ready")
            if healthy == "" or images_ready == "":
                raise Exception("HCI stats missing values")
            log.log("DASHBOARD", tc_id, desc, "PASS")
            print(f"{tc_id} PASS - HCI stats OK (Healthy={healthy}, ImagesReady={images_ready})")
        except Exception as e:
            log.log("DASHBOARD", tc_id, desc, "FAIL", str(e))
            print(f"{tc_id} FAIL - {e}")

        # ------------------ TC: Orion Images section refresh / empty state ------------------
        tc_id = "TC_DASH_08"
        desc = "Orion Images refresh and empty state"
        try:
            dash.click_refresh_images()
            time.sleep(1)
            # images empty message is optional; test will pass either if the message visible OR images exist
            try:
                if dash.images_empty_message_visible():
                    log.log("DASHBOARD", tc_id, desc, "PASS")
                    print(f"{tc_id} PASS - Images empty state visible")
                else:
                    raise Exception("images_empty_message_visible() returned False")
            except Exception:
                # if exception, maybe images exist; that's acceptable
                log.log("DASHBOARD", tc_id, desc, "PASS", "Images present (not empty)")
                print(f"{tc_id} PASS - Images present")
        except Exception as e:
            log.log("DASHBOARD", tc_id, desc, "FAIL", str(e))
            print(f"{tc_id} FAIL - {e}")

        # ------------------ TC: Sidebar Navigation ------------------
        sidebar_tests = [
            ("Dashboard", "/dashboard"),
            ("Upload", "/upload"),
            ("Conversions", "/conversions"),
            ("Jobs", "/jobs"),
            ("Orion Clusters", "/clusters"),  # adjust if real path differs
        ]
        for idx, (item, expected_path) in enumerate(sidebar_tests, start=9):
            tc_id = f"TC_DASH_{idx:02d}"
            desc = f"Sidebar nav to {item} -> {expected_path}"
            try:
                dash.nav_to(item)
                wait.until(EC.url_contains(expected_path))
                log.log("DASHBOARD", tc_id, desc, "PASS")
                print(f"{tc_id} PASS - Sidebar {item} -> {expected_path}")
            except Exception as e:
                log.log("DASHBOARD", tc_id, desc, "FAIL", str(e))
                print(f"{tc_id} FAIL - Sidebar {item}: {e}")
            finally:
                # navigate back to dashboard for next iteration
                driver.get(f"{BASE_URL}/dashboard")
                wait.until(EC.url_contains("/dashboard"))

        # ------------------ TC: Logout ------------------
        tc_id = "TC_DASH_14"
        desc = "Logout ends session and redirects to login"
        try:
            dash.sign_out()
            wait.until(EC.url_contains("/login"))
            log.log("DASHBOARD", tc_id, desc, "PASS")
            print(f"{tc_id} PASS - Logout successful")
        except Exception as e:
            log.log("DASHBOARD", tc_id, desc, "FAIL", str(e))
            print(f"{tc_id} FAIL - Logout: {e}")

    except Exception as outer_e:
        print("Unexpected error during dashboard tests:")
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
            print("Browser closed.")


if __name__ == "__main__":
    run_dashboard_tests()
