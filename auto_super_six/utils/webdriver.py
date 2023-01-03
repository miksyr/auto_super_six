import os
from typing import Optional

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


def get_default_firefox_options(run_headless: bool):
    options = Options()
    options.headless = run_headless
    options.set_preference("places.history.enabled", False)
    options.set_preference("privacy.clearOnShutdown.offlineApps", True)
    options.set_preference("privacy.clearOnShutdown.passwords", True)
    options.set_preference("privacy.clearOnShutdown.siteSettings", True)
    options.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
    return options


def get_firefox_web_driver(run_headless: bool, implicit_wait_time: int = 1, options: Optional[Options] = None):
    driver = Firefox(
        executable_path=os.environ["GECKODRIVER_PATH"],
        options=options or get_default_firefox_options(run_headless=run_headless),
    )
    driver.implicitly_wait(time_to_wait=implicit_wait_time)
    return driver
