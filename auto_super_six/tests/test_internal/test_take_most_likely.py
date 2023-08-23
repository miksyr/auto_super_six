from typing import List

import pytest
from betfair_api_client.datamodel.runner import Runner
from betfair_api_client.datamodel.runner_price import RunnerPrice
from auto_super_six.internal.picking_strategies import TakeMostLikely


@pytest.mark.parametrize(
    "back_odds, num_selections",
    [([2, 3, 4, 5], 10), ([1, 100, 200, 300, 5, 6, 67], 20)],
)
def test_take_most_likely(back_odds: List[float], num_selections: int):
    runners = []
    for back_odd in back_odds:
        runner = Runner(runnerId=1, runnerName="1", handicap=0)
        runner.update_back_odds(
            availableToBack=[RunnerPrice(betType="back", price=back_odd, size=1)]
        )
        runners.append(runner)

    strategy = TakeMostLikely()
    selections = [
        strategy.pick_selection(runners=runners) for _ in range(num_selections)
    ]
    assert len(selections) == num_selections
    assert len(set(selections)) == 1
