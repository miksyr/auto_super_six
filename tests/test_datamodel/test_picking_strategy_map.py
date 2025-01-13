import pytest

from auto_super_six.datamodel.picking_strategy_map import PickingStrategyMap
from auto_super_six.internal.picking_strategies import (
    BasePickingStrategy,
    SampleUsingProbabilities,
    TakeMostLikely,
)


@pytest.mark.parametrize(
    "strategy_name, expected_output",
    [("mle", TakeMostLikely()), ("prob", SampleUsingProbabilities())],
)
def test_get_strategy(strategy_name: str, expected_output: BasePickingStrategy):
    strategy = PickingStrategyMap.get_strategy(strategy_name=strategy_name)
    assert strategy.__class__.__name__ == expected_output.__class__.__name__
