"""Body composition and energy expenditure calculation tools."""

from pydantic import BaseModel, Field
from strands import tool

from tools.constants import ActivityLevel, Goal, Sex, UnitSystem

# --------------------------------------------------------------------------
# Request / response models
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


# --------------------------------------------------------------------------
# Unit conversion helpers
# --------------------------------------------------------------------------


def _lbs_to_kg(pounds: float) -> float:
    """Convert weight from pounds to kilograms."""
    return pounds * 0.453592


def _inches_to_cm(inches: float) -> float:
    """Convert height from inches to centimeters."""
    return inches * 2.54


def _inches_to_meters(inches: float) -> float:
    """Convert height from inches to meters."""
    return inches * 0.0254


def _cm_to_inches(cm: float) -> float:
    """Convert height from centimeters to inches."""
    return cm / 2.54


def _bmi_category(bmi: float) -> str:
    """Determine the BMI category based on the BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    return "Obesity"


# --------------------------------------------------------------------------
# Tools
# --------------------------------------------------------------------------


@tool
def calculate_bmr(request: BMRRequest) -> BMRResponse:
    """
    Calculate Basal Metabolic Rate (BMR) using the Mifflin-St Jeor Equation.

    Args:
        request: Weight, height, age, sex, and unit system of the user.

    Returns:
        The calculated BMR in kilocalories/day.
    """
    if request.unit == UnitSystem.IMPERIAL:
        weight = _lbs_to_kg(request.weight)
        height = _inches_to_cm(request.height)
    else:
        weight = request.weight
        height = request.height

    if request.sex == Sex.MALE:
        bmr = 10 * weight + 6.25 * height - 5 * request.age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * request.age - 161

    return BMRResponse(bmr=round(bmr, 1))


@tool
def calculate_bmi(request: BMIRequest) -> BMIResponse:
    """
    Calculate BMI and determine its category.

    Args:
        request: Weight, height, and unit system of the user.

    Returns:
        The BMI value and its category.
    """
    if request.unit == UnitSystem.IMPERIAL:
        weight = _lbs_to_kg(request.weight)
        height = _inches_to_meters(request.height)
    else:
        weight = request.weight
        height = request.height

    bmi = weight / (height ** 2)
    return BMIResponse(bmi=round(bmi, 1), category=_bmi_category(bmi))


@tool
def calculate_tdee(request: TDEERequest) -> TDEEResponse:
    """
    Calculate Total Daily Energy Expenditure (TDEE).

    Args:
        request: BMR and activity level of the user.

    Returns:
        The calculated TDEE in kilocalories/day.
    """
    tdee = request.bmr * request.activity_level.multiplier
    return TDEEResponse(tdee=round(tdee, 1))


@tool
def calculate_target_calories(request: TargetCaloriesRequest) -> TargetCaloriesResponse:
    """
    Calculate target daily caloric intake based on TDEE and user goal.

    Args:
        request: TDEE and goal of the user.

    Returns:
        The target daily caloric intake.
    """
    target_calories = request.tdee + request.goal.calorie_adjustment
    return TargetCaloriesResponse(target_calories=round(target_calories, 1))


@tool
def calculate_macros(request: MacroNutrientRequest) -> MacroNutrientResponse:
    """
    Calculate macronutrient distribution based on target calories and user goal.

    Args:
        request: Target daily caloric intake and goal of the user.

    Returns:
        The macronutrient distribution in grams.
    """
    protein_ratio, carb_ratio, fat_ratio = request.goal.macro_split

    protein_grams = (request.target_calories * protein_ratio) / 4
    carb_grams = (request.target_calories * carb_ratio) / 4
    fat_grams = (request.target_calories * fat_ratio) / 9

    return MacroNutrientResponse(
        protein=round(protein_grams, 1),
        fat=round(fat_grams, 1),
        carbs=round(carb_grams, 1),
    )


@tool
def calculate_ideal_weight(request: IdealWeightRequest) -> IdealWeightResponse:
    """
    Calculate ideal body weight using the Devine formula.

    Formula (height over 5 feet):
        Male:   50.0 + 2.3 kg per inch over 60 inches
        Female: 45.5 + 2.3 kg per inch over 60 inches

    Args:
        request: Height, sex, and unit system of the user.

    Returns:
        The ideal body weight in kilograms.
    """
    height_in_inches = (
        request.height if request.unit == UnitSystem.IMPERIAL else _cm_to_inches(request.height)
    )

    base_weight_kg = 50.0 if request.sex == Sex.MALE else 45.5
    ideal_weight = base_weight_kg + 2.3 * (height_in_inches - 60)

    return IdealWeightResponse(ideal_weight=round(ideal_weight, 1))
