# auto_super_six

Automatic submissions to SuperSix.

* Uses selenium to log in to the SuperSix website
* Pulls games that need predictions
* Looks up odds on Betfair for each score ("wisdom of crowds", exchanges should offer prices that are similar to "true" probabilities)
* Submit estimates to SuperSix based on a strategy (e.g. sampling based on estimated probabilities or always taking the most likely outcome)
