"""Body composition and energy expenditure calculation tools."""

from strands import tool, ToolContext

from tools.constants import Sex, UnitSystem
from tools.models import (
    BMIRequest,
    BMIResponse,
    BMRRequest,
    BMRResponse,
    IdealWeightRequest,
    IdealWeightResponse,
    MacroNutrientRequest,
    MacroNutrientResponse,
    TargetCaloriesRequest,
    TargetCaloriesResponse,
    TDEERequest,
    TDEEResponse,
)

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


@tool(context=True)
def calculate_bmr(request: BMRRequest, tool_context: ToolContext) -> BMRResponse:
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


@tool(context=True)
def calculate_bmi(request: BMIRequest, tool_context: ToolContext) -> BMIResponse:
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


@tool(context=True)
def calculate_tdee(request: TDEERequest, tool_context: ToolContext) -> TDEEResponse:
    """
    Calculate Total Daily Energy Expenditure (TDEE).

    Args:
        request: BMR and activity level of the user.

    Returns:
        The calculated TDEE in kilocalories/day.
    """
    tdee = request.bmr * request.activity_level.multiplier
    return TDEEResponse(tdee=round(tdee, 1))


@tool(context=True)
def calculate_target_calories(request: TargetCaloriesRequest, tool_context: ToolContext) -> TargetCaloriesResponse:
    """
    Calculate target daily caloric intake based on TDEE and user goal.

    Args:
        request: TDEE and goal of the user.

    Returns:
        The target daily caloric intake.
    """
    target_calories = request.tdee + request.goal.calorie_adjustment
    return TargetCaloriesResponse(target_calories=round(target_calories, 1))


@tool(context=True)
def calculate_macros(request: MacroNutrientRequest, tool_context: ToolContext) -> MacroNutrientResponse:
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


@tool(context=True)
def calculate_ideal_weight(request: IdealWeightRequest, tool_context: ToolContext) -> IdealWeightResponse:
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
