from typing import List

import numpy as np
from betfair_api_client.datamodel.runner import Runner

from auto_super_six.internal.picking_strategies import BasePickingStrategy


class SampleUsingProbabilities(BasePickingStrategy):
    def pick_selection(self, runners: List[Runner]) -> Runner:
        score_probabilities = np.array([1 / r.get_best_back_price().price for r in runners])
        renormed_score_probabilities = score_probabilities / sum(score_probabilities)
        return np.random.choice(a=runners, p=renormed_score_probabilities)
