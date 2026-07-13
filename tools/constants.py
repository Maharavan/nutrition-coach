from __future__ import annotations
from enum import Enum
from typing import Tuple

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

    @property
    def macro_split(self) -> tuple[float, float, float]:
        """Return the (protein_ratio, carb_ratio, fat_ratio) split associated with each goal."""
        return {
            Goal.LOSE_WEIGHT: (0.30, 0.45, 0.25),
            Goal.MAINTAIN_WEIGHT: (0.25, 0.45, 0.30),
            Goal.GAIN_WEIGHT: (0.25, 0.45, 0.30),
        }[self]

class Sex(str, Enum):
    """Enumeration representing the sex of the user.""" 
    MALE = "male"
    FEMALE = "female"

class UnitSystem(str, Enum):
    """Enumeration representing the unit system for measurements."""
    METRIC = "metric"
    IMPERIAL = "imperial"

class ExerciseType(str, Enum):
    """Enumeration representing different exercise types."""
    WALKING = "walking"
    BRISK_WALKING = "brisk walking"
    RUNNING = "running"
    CYCLING = "cycling"
    SWIMMING = "swimming"
    YOGA = "yoga"
    STRENGTH_TRAINING = "strength training"
    @property
    def met(self) -> float:
        """Return the MET (Metabolic Equivalent of Task) value associated with this exercise type."""
        return {
            ExerciseType.WALKING: 3.5,
            ExerciseType.BRISK_WALKING: 4.3,
            ExerciseType.RUNNING: 8.3,
            ExerciseType.CYCLING: 8.0,
            ExerciseType.SWIMMING: 6.0,
            ExerciseType.YOGA: 2.5,
            ExerciseType.STRENGTH_TRAINING: 6.0,
        }[self]