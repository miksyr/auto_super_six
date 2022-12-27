import sys
sys.path.append("../../")
import os

from betfair_api_client import BetfairApiClient
import fire

from auto_super_six.datamodel.super_six_competition import SuperSixCompetition
from auto_super_six.datamodel.picking_strategy_map import PickingStrategyMap
from auto_super_six.internal.super_six_webpage import SuperSixWebpage
from auto_super_six.utils.betfair_events import get_betfair_event
from auto_super_six.utils.webdriver import get_firefox_web_driver


def submit_predictions(strategy_name: str = "mle"):

    strategy = PickingStrategyMap.get_strategy(strategy_name=strategy_name)

    with get_firefox_web_driver(run_headless=False) as web_driver:
        super_six_webpage = SuperSixWebpage(web_driver=web_driver)
        super_six_webpage.login(
            username=os.environ["SUPER_SIX_USERNAME"],
            pin_code=os.environ["SUPER_SIX_PIN"],
        )
        matches_to_predict = super_six_webpage.get_matches_to_predict()

        betfair_client = BetfairApiClient(
            username=os.environ["BETFAIR_USERNAME"],
            password=os.environ["BETFAIR_PASSWORD"],
            apiKey=os.environ["BETFAIR_API_KEY"],
            clientCertificatePath=os.environ["BETFAIR_CLIENT_CERT"],
            certificateKeyPath=os.environ["BETFAIR_CLIENT_CERT_KEY"],
        )

        correct_score_predictions = []
        for match in matches_to_predict:
            competition = SuperSixCompetition.get_competition_enum(
                competition_name=super_six_webpage.get_competition(
                    match_container_element=match
                )
            )
            home_team_name, away_team_name = super_six_webpage.get_team_names(
                match_container_element=match
            )
            betfair_event = get_betfair_event(
                betfair_client=betfair_client,
                home_team_name=home_team_name,
                away_team_name=away_team_name,
                competition_id=competition.betfair_competition_id,
            )
            betfair_client.update_prices_for_events(events=[betfair_event])
            all_correct_score_runners = betfair_event.get_all_markets()[0].get_all_runners()
            numeric_only_score_runners = [
                r for r in all_correct_score_runners if "-" in r.runnerName
            ]
            runner_choice = strategy.pick_selection(runners=numeric_only_score_runners)
            correct_score_predictions.append(runner_choice)

        super_six_webpage.submit_match_predictions(
            score_predictions=tuple(
                score.runnerName.split(" - ", 1) for score in correct_score_predictions
            ),
            golden_goal_minute=15,
        )


if __name__ == "__main__":
    fire.Fire(submit_predictions)
