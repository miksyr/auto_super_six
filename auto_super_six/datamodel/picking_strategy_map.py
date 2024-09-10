from enum import Enum

from auto_super_six.internal.picking_strategies import (
    BasePickingStrategy,
    SampleTopNProbabilities,
    SampleUsingProbabilities,
    TakeMostLikely,
)


class StrategyNotFound(Exception):
    pass


class PickingStrategyMap(Enum):
    mle = TakeMostLikely
    prob = SampleUsingProbabilities
    sample_topn = SampleTopNProbabilities

    @classmethod
    def get_strategy(cls, strategy_name: str) -> BasePickingStrategy:
        for strategy in cls:
            if strategy.name == strategy_name:
                return strategy.value()
        raise StrategyNotFound(f"{strategy_name} not found.  Use one of; {cls.enum_members}")
