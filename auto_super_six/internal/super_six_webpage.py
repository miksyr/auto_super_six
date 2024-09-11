from time import sleep
from typing import List, Tuple

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from auto_super_six.datamodel.home_or_away import HomeOrAway


class SuperSixWebpage:
    def __init__(
        self,
        web_driver: WebDriver,
        super_six_url: str = "https://super6.skysports.com/",
    ):
        self.web_driver = web_driver
        self.super_six_url = super_six_url
        self.web_driver.get(url=super_six_url)

    def _accept_cookies(self) -> None:
        cookies_elem = WebDriverWait(driver=self.web_driver, timeout=30).until(
            method=EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        self.web_driver.execute_script("arguments[0].click();", cookies_elem)

    def login(self, username: str, pin_code: str) -> None:
        self._accept_cookies()
        self.web_driver.find_element(by=By.ID, value="account-bar-login-btn").click()
        self.web_driver.find_element(by=By.ID, value="username").send_keys(username)
        self.web_driver.find_element(by=By.ID, value="pin").send_keys(pin_code)
        self.web_driver.find_element(by=By.ID, value="login-submit").click()
        sleep(2)

    def _get_teams_for_prediction(self, home_or_away: HomeOrAway) -> List[str]:
        teams = []
        for v in self.web_driver.find_elements(by=By.XPATH, value=f"//*[contains(@id, '-team-{home_or_away.value}')]"):
            if v.text:
                teams.append(v.text.lower())
        return teams

    def get_matches_to_predict(self) -> List[WebElement]:
        self.web_driver.get(f"{self.super_six_url}/play")
        sleep(2)
        return self.web_driver.find_elements(by=By.XPATH, value="//*[contains(@data-test-id, 'match-container-')]")

    @staticmethod
    def get_competition(match_container_element: WebElement) -> str:
        return match_container_element.text.split("\n", 1)[0]

    @staticmethod
    def get_team_names(match_container_element: WebElement) -> Tuple[str, ...]:
        team_containers = match_container_element.find_elements(by=By.CLASS_NAME, value="team-container")
        return tuple(v.text.lower() for v in team_containers)

    def is_already_submitted(self) -> bool:
        self.web_driver.get(f"{self.super_six_url}/play")
        try:
            self.web_driver.find_element(
                by=By.XPATH,
                value="//button[contains(@data-test-id, 'show-predictions-edit-button')]",
            )
            return True
        except NoSuchElementException:
            return False

    def input_match_predictions(self, score_predictions: Tuple[List[int]]) -> None:
        self.web_driver.get(f"{self.super_six_url}/play")
        sleep(2)
        home_team_score_elements = self.web_driver.find_elements(
            by=By.XPATH,
            value="//button[contains(@data-test-id, 'match-team-prediction-home-increase')]",
        )
        away_team_score_elements = self.web_driver.find_elements(
            by=By.XPATH,
            value="//button[contains(@data-test-id, 'match-team-prediction-away-increase')]",
        )

        for score_prediction, home_team_score_elem, away_team_score_elem in zip(
            score_predictions, home_team_score_elements, away_team_score_elements
        ):
            for _ in range(int(score_prediction[0])):
                home_team_score_elem.click()

            for _ in range(int(score_prediction[1])):
                away_team_score_elem.click()

    def input_golden_goal_minute(self, golden_goal_minute: int) -> None:
        golden_goal_element = self.web_driver.find_element(
            by=By.XPATH, value="//input[@data-test-id = 'play-golden-goal-input']"
        )
        golden_goal_element.clear()
        golden_goal_element.send_keys(golden_goal_minute)

    def submit_predictions(self) -> None:
        sleep(1)
        self.web_driver.find_element(by=By.ID, value="js-fixtures-submit-entry").click()
