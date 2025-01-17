from typing import List

import numpy as np
from betfair_api_client.datamodel.runner import Runner

from auto_super_six.internal.picking_strategies import BasePickingStrategy


class SampleTopNProbabilities(BasePickingStrategy):

    def __init__(self, n: int = 3):
        self.n = n

    def pick_selection(self, runners: List[Runner]) -> Runner:
        top_n_runners = sorted(runners, key=lambda x: x.get_best_back_price().price)[:self.n]
        score_probabilities = np.array([1 / r.get_best_back_price().price for r in top_n_runners])
        renormed_score_probabilities = score_probabilities / sum(score_probabilities)
        return np.random.choice(a=top_n_runners, p=renormed_score_probabilities)
