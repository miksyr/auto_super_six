from enum import Enum

from auto_super_six.internal.picking_strategies import (
    BasePickingStrategy,
    SampleUsingProbabilities,
    TakeMostLikely,
)


class StrategyNotFound(Exception):
    pass


class PickingStrategyMap(Enum):

    prob = SampleUsingProbabilities
    mle = TakeMostLikely

    @classmethod
    def get_strategy(cls, strategy_name: str) -> BasePickingStrategy:
        for strategy in cls:
            if strategy.name == strategy_name:
                return strategy.value
        raise StrategyNotFound(
            f"{strategy_name} not found.  Use one of; {cls.enum_members}"
        )
