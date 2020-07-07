# Slay-I

> For the mod that runs inference on the model in the game, see https://github.com/alexdriedger/SlayTheSpireFightPredictorMod

Slay the Spire + Neural Networks. Available on the [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=2157144906)!

Slay-I uses a machine learning model trained on over 325, 000 fights!

## Predict Damage Taken in a Fight

![Ironclad Fight Prediction](https://raw.githubusercontent.com/alexdriedger/SlayTheSpireFightPredictorMod/master/workshopImages/Fight%20Prediction%20Lag.jpg)

![Silent Fight Prediction](https://raw.githubusercontent.com/alexdriedger/SlayTheSpireFightPredictorMod/master/workshopImages/Fight%20Prediction%20Slime%20Silent.jpg)

## Evaluating Cards

Slay-I evaluates cards based on average damage saved in a fight if the card is added to your deck.

![Silend Card Reward](https://raw.githubusercontent.com/alexdriedger/SlayTheSpireFightPredictorMod/master/workshopImages/Card%20Add%20Silent.jpg)

![Ironclad Card Reward](https://raw.githubusercontent.com/alexdriedger/SlayTheSpireFightPredictorMod/master/workshopImages/Card%20Add%20One%20Bad.jpg)

## Upgrades and Removals

Slay-I also evaluates upgrading and removing cards

![Silent Card Removal](https://raw.githubusercontent.com/alexdriedger/SlayTheSpireFightPredictorMod/master/workshopImages/Card%20Removal%20Silent.jpg)

## Data Set

Data is from [Spire Logs](https://spirelogs.com/) and [Jorbs](https://www.youtube.com/user/JoINrbs).

## Accuracy

Slay-I is generally within +/- 7 HP of how much damage you will take in a fight. For adding, removing, and upgrading cards, the score is the average damage saved in a fight. The model isn't perfect, but it does a pretty good job at evaluating cards!
