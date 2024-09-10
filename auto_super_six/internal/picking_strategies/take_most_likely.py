from typing import List

import numpy as np
from betfair_api_client.datamodel.runner import Runner

from auto_super_six.internal.picking_strategies import BasePickingStrategy


class TakeMostLikely(BasePickingStrategy):
    def pick_selection(self, runners: List[Runner]) -> Runner:
        odds = np.array([r.get_best_back_price().price for r in runners])
        return runners[np.argmin(odds)]
