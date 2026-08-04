"""
conftest.py

Shared pytest fixtures:
  - `driver`: a Chrome WebDriver instance, headless by default.
    Set HEADLESS=false to watch the browser locally.
  - `base_url`: the URL under test. Defaults to the local Flask app,
    but can point at a deployed instance by setting BASE_URL.
"""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()

    headless = os.environ.get("HEADLESS", "true").lower() == "true"
    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1280,900")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Selenium 4.6+ ships "Selenium Manager", which auto-downloads the
    # matching chromedriver binary -- no manual driver setup needed.
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


@pytest.fixture
def base_url():
    return os.environ.get("BASE_URL", "http://localhost:5000")
