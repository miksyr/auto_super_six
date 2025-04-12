from time import sleep

from selenium.common.exceptions import (
    JavascriptException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SuperSixWebpage:
    def __init__(
        self,
        web_driver: WebDriver,
        super_six_url: str = "https://super6.skysports.com/",
        timeout: int = 60,
    ):
        self.web_driver = web_driver
        self.super_six_url = super_six_url
        self.timeout = timeout
        self.web_driver.get(url=super_six_url)
        self._wait_for_page_load()

    def _wait_for_page_load(self) -> None:
        WebDriverWait(driver=self.web_driver, timeout=self.timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        sleep(2)  # wait for JavaScript to finish executing
        try:
            jquery_exists = self.web_driver.execute_script("return typeof jQuery !== 'undefined'")
            if jquery_exists:
                # If jQuery exists, wait for AJAX requests to complete
                WebDriverWait(driver=self.web_driver, timeout=self.timeout).until(
                    lambda driver: driver.execute_script("return jQuery.active == 0")
                )
        except (JavascriptException, WebDriverException, TimeoutException):
            # If jQuery is not available or there's an error checking for it,
            # continue without waiting for AJAX. This is expected on some pages
            # that don't use jQuery or when JavaScript execution fails
            pass

    def _wait_for_element(self, by: By, value: str, condition: EC = EC.presence_of_element_located):
        try:
            return WebDriverWait(driver=self.web_driver, timeout=self.timeout).until(condition((by, value)))
        except TimeoutException:
            self.web_driver.refresh()
            self._wait_for_page_load()
            return WebDriverWait(driver=self.web_driver, timeout=self.timeout).until(condition((by, value)))

    def _accept_cookies(self) -> None:
        cookies_elem = self._wait_for_element(
            by=By.ID, value="onetrust-accept-btn-handler", condition=EC.element_to_be_clickable
        )
        self.web_driver.execute_script("arguments[0].click();", cookies_elem)
        sleep(1)

    def login(self, username: str, pin_code: str) -> None:
        self._accept_cookies()
        login = self._wait_for_element(by=By.ID, value="account-bar-login-btn", condition=EC.element_to_be_clickable)
        self.web_driver.execute_script("arguments[0].click();", login)
        sleep(2)
        username_field = self._wait_for_element(by=By.ID, value="username", condition=EC.visibility_of_element_located)
        pin_field = self._wait_for_element(by=By.ID, value="pin", condition=EC.visibility_of_element_located)
        username_field.send_keys(username)
        pin_field.send_keys(pin_code)
        login_submit = self._wait_for_element(by=By.ID, value="login-submit", condition=EC.element_to_be_clickable)
        self.web_driver.execute_script("arguments[0].click();", login_submit)
        sleep(3)
        self._wait_for_page_load()

    def get_matches_to_predict(self) -> list[WebElement]:
        self.web_driver.get(f"{self.super_six_url}/play")
        self._wait_for_page_load()
        sleep(2)

        matches = self._wait_for_element(
            by=By.XPATH,
            value="//*[contains(@data-test-id, 'match-container-')]",
            condition=EC.visibility_of_all_elements_located,
        )

        if not matches:
            self.web_driver.refresh()
            self._wait_for_page_load()
            sleep(2)
            matches = self._wait_for_element(
                by=By.XPATH,
                value="//*[contains(@data-test-id, 'match-container-')]",
                condition=EC.visibility_of_all_elements_located,
            )
            if not matches:
                raise RuntimeError("No matches found after refresh attempt")

        return matches

    @staticmethod
    def get_competition(match_container_element: WebElement) -> str:
        return match_container_element.text.split("\n", 1)[0]

    @staticmethod
    def get_team_names(match_container_element: WebElement) -> tuple[str, ...]:
        team_containers = match_container_element.find_elements(by=By.CLASS_NAME, value="team-container")
        return tuple(v.text.lower() for v in team_containers)

    def is_already_submitted(self) -> bool:
        self.web_driver.get(f"{self.super_six_url}/play")
        self._wait_for_page_load()
        sleep(2)

        try:
            self._wait_for_element(
                by=By.XPATH,
                value="//button[contains(@data-test-id, 'show-predictions-edit-button')]",
                condition=EC.presence_of_element_located,
            )
            return True
        except TimeoutException:
            return False

    def input_match_predictions(self, score_predictions: tuple[list[int]]) -> None:
        self.web_driver.get(f"{self.super_six_url}/play")
        self._wait_for_page_load()
        sleep(2)

        home_team_score_elements = self._wait_for_element(
            by=By.XPATH,
            value="//button[contains(@data-test-id, 'match-team-prediction-home-increase')]",
            condition=EC.visibility_of_all_elements_located,
        )
        away_team_score_elements = self._wait_for_element(
            by=By.XPATH,
            value="//button[contains(@data-test-id, 'match-team-prediction-away-increase')]",
            condition=EC.visibility_of_all_elements_located,
        )

        for score_prediction, home_team_score_elem, away_team_score_elem in zip(
            score_predictions, home_team_score_elements, away_team_score_elements
        ):
            for _ in range(int(score_prediction[0])):
                home_team_score_elem.click()
                sleep(0.2)

            for _ in range(int(score_prediction[1])):
                away_team_score_elem.click()
                sleep(0.2)

    def input_golden_goal_minute(self, golden_goal_minute: int) -> None:
        golden_goal_element = self._wait_for_element(
            by=By.XPATH, value="//input[@data-test-id = 'play-golden-goal-input']", condition=EC.visibility_of_element_located
        )
        golden_goal_element.clear()
        golden_goal_element.send_keys(golden_goal_minute)

    def submit_predictions(self) -> None:
        submit_button = self._wait_for_element(
            by=By.ID, value="js-fixtures-submit-entry", condition=EC.element_to_be_clickable
        )
        submit_button.click()
        self._wait_for_page_load()
