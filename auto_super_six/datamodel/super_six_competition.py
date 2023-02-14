from __future__ import annotations
from enum import Enum


class CompetitionNotFound(Exception):
    pass


class SuperSixCompetition(Enum):
    PREMIER_LEAGUE = ("Premier League", 10932509)
    UEFA_CHAMPIONS_LEAGUE = ("UEFA Champions League", 228)
    CHAMPIONS_LEAGUE = ("Champions League", 228)
    EUROPA_LEAGUE = ("Europa League", 2005)
    CARABAO_CUP = ("Carabao Cup", 2134)
    WORLD_CUP = ("FIFA World Cup", 12469077)
    FA_CUP = ("FA Cup", 30558)
    CHAMPIONSHIP = ("Sky Bet Championship", 7129730)

    def __init__(self, competition_name: str, betfair_competition_id: int):
        self.competition_name = competition_name
        self.betfair_competition_id = betfair_competition_id

    @classmethod
    def get_competition_enum(cls, competition_name: str) -> SuperSixCompetition:
        for competition in cls:
            if competition.competition_name == competition_name:
                return competition
        raise CompetitionNotFound(competition_name)
