from betfair_api_client import BetfairApiClient
from betfair_api_client.datamodel.market_types import MarketTypes


def _match_by_text_query(
    betfair_client: BetfairApiClient, text_query: str, competition_id: int
):
    betfair_events = betfair_client.get_coming_events(
        sportTypeId=1,
        marketTypes=[MarketTypes.FULLTIME_SCORELINE],
        competitionIds=[competition_id],
        textQuery=text_query,
        daysAhead=7,
    )
    if len(betfair_events) != 1:
        raise IndexError(f"{len(betfair_events)} events found for {text_query}")
    return betfair_events[0]


def get_betfair_event(
    betfair_client: BetfairApiClient,
    home_team_name: str,
    away_team_name: str,
    competition_id: int,
):
    try:
        full_match = f"{home_team_name} v {away_team_name}"
        return _match_by_text_query(
            betfair_client=betfair_client,
            text_query=full_match,
            competition_id=competition_id,
        )
    except IndexError:
        try:
            return _match_by_text_query(
                betfair_client=betfair_client,
                text_query=home_team_name,
                competition_id=competition_id,
            )
        except IndexError:
            return _match_by_text_query(
                betfair_client=betfair_client,
                text_query=away_team_name,
                competition_id=competition_id,
            )
