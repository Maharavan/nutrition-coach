"""Pydantic request/response models for the tools package."""

from pydantic import BaseModel, Field

from tools.constants import ActivityLevel, ExerciseType, Goal, Sex, UnitSystem

# --------------------------------------------------------------------------
# Body metrics models
# --------------------------------------------------------------------------


class BodyMeasurementRequest(BaseModel):
    """Base request for calculations that require weight and a unit system."""

    weight: float = Field(..., gt=0, description="Weight of the user in kilograms or pounds")
    unit: UnitSystem = Field(..., description="Unit system for weight and height: 'metric' or 'imperial'")


class BMIRequest(BodyMeasurementRequest):
    """Request for a BMI calculation."""

    height: float = Field(..., gt=0, description="Height of the user in meters or inches")


class BMIResponse(BaseModel):
    """Result of a BMI calculation."""

    bmi: float = Field(..., description="Calculated Body Mass Index (BMI)")
    category: str = Field(..., description="BMI category based on the calculated BMI value")


class BMRRequest(BodyMeasurementRequest):
    """Request for a BMR calculation."""

    height: float = Field(..., gt=0, description="Height of the user in centimeters or inches")
    age: int = Field(..., gt=0, description="Age of the user in years")
    sex: Sex = Field(..., description="Sex of the user: 'male' or 'female'")


class BMRResponse(BaseModel):
    """Result of a BMR calculation."""

    bmr: float = Field(..., description="Calculated Basal Metabolic Rate (BMR)")


class TDEERequest(BaseModel):
    """Request for a TDEE calculation."""

    bmr: float = Field(..., gt=0, description="Basal Metabolic Rate (BMR) of the user")
    activity_level: ActivityLevel = Field(..., description="Activity level of the user")


class TDEEResponse(BaseModel):
    """Result of a TDEE calculation."""

    tdee: float = Field(..., description="Calculated Total Daily Energy Expenditure (TDEE)")


class TargetCaloriesRequest(BaseModel):
    """Request for a target daily caloric intake calculation."""

    tdee: float = Field(..., gt=0, description="Total Daily Energy Expenditure (TDEE) of the user")
    goal: Goal = Field(..., description="User's goal: 'lose weight', 'maintain weight', or 'gain weight'")


class TargetCaloriesResponse(BaseModel):
    """Result of a target daily caloric intake calculation."""

    target_calories: float = Field(..., description="Calculated target daily caloric intake")


class MacroNutrientRequest(BaseModel):
    """Request for a macronutrient distribution calculation."""

    target_calories: float = Field(..., gt=0, description="Target daily caloric intake")
    goal: Goal = Field(..., description="User's goal: 'lose weight', 'maintain weight', or 'gain weight'")


class MacroNutrientResponse(BaseModel):
    """Result of a macronutrient distribution calculation."""

    protein: float = Field(..., description="Calculated protein intake in grams")
    fat: float = Field(..., description="Calculated fat intake in grams")
    carbs: float = Field(..., description="Calculated carbohydrate intake in grams")


class IdealWeightRequest(BaseModel):
    """Request for an ideal body weight calculation."""

    height: float = Field(..., gt=0, description="Height of the user in centimeters or inches")
    sex: Sex = Field(..., description="Sex of the user: 'male' or 'female'")
    unit: UnitSystem = Field(..., description="Unit system for height: 'metric' or 'imperial'")


class IdealWeightResponse(BaseModel):
    """Result of an ideal body weight calculation."""

    ideal_weight: float = Field(..., description="Ideal body weight in kilograms, per the Devine formula")


class CaloriesBurnedRequest(BodyMeasurementRequest):
    """Request for an estimated calories burned calculation."""

    duration_minutes: float = Field(..., gt=0, description="Duration of the activity in minutes")
    exercise_type: ExerciseType = Field(..., description="Type of exercise performed")


class CaloriesBurnedResponse(BaseModel):
    """Result of an estimated calories burned calculation."""

    calories_burned: float = Field(..., description="Estimated calories burned during the activity")


# --------------------------------------------------------------------------
# Exercise recommendation models
# --------------------------------------------------------------------------


class WorkoutRequest(BaseModel):
    """Request to generate a personalized workout recommendation."""

    requirements: str = Field(
        ..., description="User's fitness goals, available equipment, time constraints, and experience level"
    )


class WorkoutResponse(BaseModel):
    """A personalized workout recommendation."""

    workout_plan: str = Field(..., description="The generated workout recommendation")


class ExerciseRecommendationRequest(BaseModel):
    """Request to recommend an exercise."""

    query: str = Field(
        ..., description="Target muscle group, movement goal, or constraint to recommend an exercise for"
    )


class ExerciseRecommendationResponse(BaseModel):
    """A recommended exercise."""

    recommendation: str = Field(..., description="The recommended exercise with guidance on form and reps")


class RecoveryPlanRequest(BaseModel):
    """Request to generate a recovery plan."""

    details: str = Field(..., description="Details about the workout performed, soreness, injuries, or fatigue level")


class RecoveryPlanResponse(BaseModel):
    """A personalized recovery plan."""

    recovery_plan: str = Field(..., description="The generated recovery plan")


# --------------------------------------------------------------------------
# Nutrition models
# --------------------------------------------------------------------------


class FoodNutritionRequest(BaseModel):
    """Request to look up nutritional information for a food."""

    food_name: str = Field(..., description="Name of the food to look up nutritional information for")


class MealAnalysisRequest(BaseModel):
    """Request to analyze a meal."""

    meal: str = Field(..., description="Description of the meal to analyze")


class MealPlanRequest(BaseModel):
    """Request to generate a personalized meal plan."""

    requirements: str = Field(
        ..., description="User's goals, calorie target, dietary preferences, allergies, and lifestyle"
    )


class RecipeRequest(BaseModel):
    """Request to generate a healthy recipe."""

    request: str = Field(..., description="Desired recipe, e.g. ingredients on hand or dietary constraints")


class FoodSwapRequest(BaseModel):
    """Request for healthier alternatives to a food."""

    food: str = Field(..., description="Food to find healthier alternatives for")


class NutritionResearchRequest(BaseModel):
    """Request to research a nutrition question."""

    question: str = Field(..., description="Nutrition-related question to research")


class NutritionInfoResponse(BaseModel):
    """Nutritional information for a food."""

    food_name: str = Field(..., description="The food that was looked up")
    info: str = Field(..., description="Nutritional information including calories and macronutrients")


class MealAnalysisResponse(BaseModel):
    """Nutritional analysis of a meal."""

    analysis: str = Field(..., description="Estimated calories, macronutrients, and feedback for the meal")


class MealPlanResponse(BaseModel):
    """A personalized meal plan."""

    meal_plan: str = Field(..., description="The generated meal plan")


class RecipeResponse(BaseModel):
    """A healthy recipe recommendation."""

    recipe: str = Field(..., description="Ingredients, preparation steps, and estimated nutrition")


class FoodSwapResponse(BaseModel):
    """Healthier alternatives for a food."""

    suggestions: str = Field(..., description="Recommended healthier alternatives")


class NutritionResearchResponse(BaseModel):
    """Answer to a nutrition research question."""

    answer: str = Field(..., description="Answer synthesized from research")


# --------------------------------------------------------------------------
# Health research models
# --------------------------------------------------------------------------


class HealthResearchRequest(BaseModel):
    """Request to research a health question."""

    question: str = Field(..., description="Health-related question to research")


class HealthResearchResponse(BaseModel):
    """Answer to a health research question."""

    answer: str = Field(..., description="Answer synthesized from research")


class FactCheckRequest(BaseModel):
    """Request to fact-check a health claim."""

    claim: str = Field(..., description="Health claim to verify")


class FactCheckResponse(BaseModel):
    """Result of fact-checking a health claim."""

    verdict: str = Field(..., description="Verdict and reasoning synthesized from research")


# --------------------------------------------------------------------------
# Motivation models
# --------------------------------------------------------------------------


class MotivationRequest(BaseModel):
    """Request for a daily motivational message."""

    context: str = Field(
        default="", description="Optional context about the user's goals, mood, or current challenges"
    )


class MotivationResponse(BaseModel):
    """A daily motivational message."""

    message: str = Field(..., description="The generated motivational message")


class HealthyHabitTipRequest(BaseModel):
    """Request for a healthy habit tip."""

    category: str = Field(
        default="", description="Optional focus area for the tip, e.g. sleep, hydration, exercise, or stress"
    )


class HealthyHabitTipResponse(BaseModel):
    """A healthy habit tip."""

    tip: str = Field(..., description="The generated healthy habit tip")