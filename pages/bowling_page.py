"""
pages/bowling_page.py

Page Object for the bowling scorer web UI. Keeps every locator in one
place so tests read like plain English and stay easy to maintain.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BowlingPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def load(self):
        self.driver.get(self.base_url)

    def enter_frame(self, index: int, value: str):
        box = self.driver.find_element(By.ID, f"frame-{index}")
        box.clear()
        box.send_keys(value)

    def enter_frames(self, frames):
        """frames: a list of roll-lists, e.g. [["8", "/"], ["5", "4"], ...]"""
        for i, frame in enumerate(frames):
            self.enter_frame(i, ",".join(frame))

    def submit(self):
        self.driver.find_element(By.ID, "calculate-btn").click()

    def get_final_score(self, timeout=5) -> str:
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.visibility_of_element_located((By.ID, "final-score")))
        return element.text

    def get_cumulative_score(self, frame_index: int) -> str:
        return self.driver.find_element(By.ID, f"score-{frame_index}").text

    def get_error_message(self, timeout=3):
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located((By.ID, "error-message")))
            return element.text
        except TimeoutException:
            return None
