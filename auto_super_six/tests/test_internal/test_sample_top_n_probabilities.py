from typing import List

import pytest
from betfair_api_client.datamodel.runner import Runner
from betfair_api_client.datamodel.runner_price import RunnerPrice

from auto_super_six.internal.picking_strategies import SampleTopNProbabilities

# sampling a few times to ensure consistency
NUM_SELECTIONS = 10


@pytest.mark.parametrize(
    "back_odds, n, top_n_odds",
    [([2, 4, 3, 5], 2, [2, 3]), ([1, 100, 200, 300, 5, 6, 67], 4, [1, 5, 6, 67])],
)
def test_sample_top_n_probabilities(back_odds: List[float], n: int, top_n_odds: List[int]):
    runners = []
    for i, back_odd in enumerate(back_odds):
        runner = Runner(runnerId=i, runnerName="i", handicap=0)
        runner.update_back_odds(availableToBack=[RunnerPrice(betType="back", price=back_odd, size=1)])
        runners.append(runner)

    strategy = SampleTopNProbabilities()
    selections = [strategy.pick_selection(runners=runners, n=n) for _ in range(NUM_SELECTIONS)]
    assert len(selections) == NUM_SELECTIONS
    assert len(set(selections)) > 1
    for s in selections:
        assert s.get_best_back_price().price in top_n_odds
