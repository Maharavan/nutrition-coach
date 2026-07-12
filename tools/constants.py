from enum import Enum

class ActivityLevel(str, Enum):
    """Enumeration representing different activity levels."""
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly active"
    MODERATELY_ACTIVE = "moderately active"
    VERY_ACTIVE = "very active"
    EXTRA_ACTIVE = "extra active"
    @property
    def multiplier(self) -> float:
        """Return the multiplier associated with each activity level."""
        return {
            ActivityLevel.SEDENTARY: 1.2,
            ActivityLevel.LIGHTLY_ACTIVE: 1.375,
            ActivityLevel.MODERATELY_ACTIVE: 1.55,
            ActivityLevel.VERY_ACTIVE: 1.725,
            ActivityLevel.EXTRA_ACTIVE: 1.9
        }[self]

class Goal(str, Enum):
    """Enumeration representing different user goals for caloric intake."""
    LOSE_WEIGHT = "lose weight"
    MAINTAIN_WEIGHT = "maintain weight"
    GAIN_WEIGHT = "gain weight"
    @property
    def calorie_adjustment(self) -> float:
        """Return the calorie adjustment associated with each goal."""
        return {
            Goal.LOSE_WEIGHT: -500,
            Goal.MAINTAIN_WEIGHT: 0,
            Goal.GAIN_WEIGHT: 500
        }[self]

class Sex(str, Enum):
    """Enumeration representing the sex of the user.""" 
    MALE = "male"
    FEMALE = "female"

class UnitSystem(str, Enum):
    """Enumeration representing the unit system for measurements."""
    METRIC = "metric"
    IMPERIAL = "imperial"
