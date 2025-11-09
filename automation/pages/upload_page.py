from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time, os

class DashboardPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # ---------------- BASIC PAGE CHECKS ----------------
    def verify_dashboard_loaded(self):
        """
        Verify that the dashboard is loaded successfully after login.
        """
        try:
            self.wait.until(EC.url_contains("/dashboard"))
            self.wait.until(
                lambda d: d.find_element(
                    By.XPATH,
                    '//*[contains(normalize-space(.),"Dashboard") or contains(normalize-space(.),"Welcome back")]'
                )
            )
            return True
        except Exception:
            return False

    def is_loaded(self):
        return "/dashboard" in self.driver.current_url

    # ---------------- DASHBOARD ACTION BUTTONS ----------------
    def click_upload_files(self):
        btn = self.wait.until(
            lambda d: d.find_element(
                By.XPATH, '//*[self::button or self::a][contains(.,"Upload Files")]'
            )
        )
        btn.click()

    def click_view_conversions(self):
        btn = self.wait.until(
            lambda d: d.find_element(
                By.XPATH, '//*[self::button or self::a][contains(.,"View Conversions")]'
            )
        )
        btn.click()

    def click_job_queue(self):
        btn = self.wait.until(
            lambda d: d.find_element(
                By.XPATH, '//*[self::button or self::a][contains(.,"Job Queue")]'
            )
        )
        btn.click()

    # ---------------- SIDEBAR NAVIGATION ----------------
    def nav_to(self, menu_name: str):
        """
        Click a left sidebar nav item by visible text.
        Examples: "Dashboard", "Upload", "Conversions", "Jobs", "Orion Clusters"
        """
        link = self.wait.until(
            lambda d: d.find_element(
                By.XPATH,
                f'//nav//a[normalize-space()="{menu_name}"] | //nav//*[self::a or self::div][contains(normalize-space(.),"{menu_name}")]'
            )
        )
        link.click()

    def sign_out(self):
        logout = self.wait.until(
            lambda d: d.find_element(
                By.XPATH, '//a[contains(.,"Sign out") or contains(.,"Sign Out")]'
            )
        )
        logout.click()

    # ---------------- STATS CARDS ----------------
    def get_conversion_stats_card(self):
        return self.wait.until(
            lambda d: d.find_element(By.XPATH, '//*[contains(.,"Conversion Stats")]')
        )

    def get_job_stats_card(self):
        return self.wait.until(
            lambda d: d.find_element(By.XPATH, '//*[contains(.,"Job Stats")]')
        )

    def get_hci_stats_card(self):
        return self.wait.until(
            lambda d: d.find_element(By.XPATH, '//*[contains(.,"Orion HCI Stats")]')
        )

    def get_orion_images_card(self):
        return self.wait.until(
            lambda d: d.find_element(By.XPATH, '//*[contains(.,"Orion Images")]')
        )

    # ---------------- STATS VALUE FETCHER ----------------
    def get_stat_value_by_label(self, card_el, label_text):
        """
        Find the value adjacent to a label inside a stats card.
        """
        try:
            el = card_el.find_element(
                By.XPATH,
                f'.//*[contains(normalize-space(.),"{label_text}")]/following::*[1]'
            )
            return el.text.strip()
        except Exception:
            return ""

    # ---------------- ORION IMAGES ----------------
    def click_refresh_images(self):
        btn = self.wait.until(
            lambda d: d.find_element(By.XPATH, '//*[contains(.,"Refresh")]')
        )
        btn.click()
        time.sleep(1)

    def images_empty_message_visible(self):
        try:
            self.wait.until(
                lambda d: d.find_element(By.XPATH, '//*[contains(.,"No images found")]')
            )
            return True
        except Exception:
            return False

    # ---------------- UPLOAD PAGE HELPERS (optional, for convenience) ----------------
    def upload_file(self, file_path: str):
        """
        Use this only when you are on the /upload page.
        Selects file and clicks Upload/Submit, then waits for success message.
        """
        if not os.path.exists(file_path):
            raise Exception(f"File not found: {file_path}")

        file_input = self.wait.until(
            lambda d: d.find_element(By.XPATH, '//input[@type="file"]')
        )
        file_input.send_keys(file_path)
        time.sleep(1)

        upload_btn = self.wait.until(
            lambda d: d.find_element(
                By.XPATH, '//*[self::button or self::a][contains(.,"Upload") or contains(.,"Submit")]'
            )
        )
        upload_btn.click()

        # success toast/message
        self.wait.until(
            lambda d: d.find_element(
                By.XPATH, '//*[contains(.,"Upload successful") or contains(.,"File uploaded")]'
            )
        )
        return True
