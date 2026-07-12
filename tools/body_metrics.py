from pydantic import BaseModel, Field
from strands import tool
from tools.constants import ActivityLevel, Goal, Sex, UnitSystem

class BodyMeasurementRequest(BaseModel):
    """Model representing a request for body metrics calculations."""
    weight: float = Field(..., gt=0, description="Weight of the user in kilograms or pounds")
    unit: UnitSystem = Field(..., description="Unit system for weight and height: 'metric' or 'imperial'")

class BMIRequest(BodyMeasurementRequest):
    """Model representing a BMI calculation request."""
    height: float = Field(..., gt=0, description="Height of the user in meters or inches")

class BMIResponse(BaseModel):
    """Model representing a BMI calculation response."""
    bmi: float = Field(..., description="Calculated Body Mass Index (BMI)")
    category: str = Field(..., description="BMI category based on the calculated BMI value")

class BMRRequest(BodyMeasurementRequest):
    """Model representing a BMR calculation request."""
    height: float = Field(..., gt=0, description="Height of the user in centimeters or inches")
    age: int = Field(..., gt=0, description="Age of the user in years")
    sex: Sex = Field(..., description="Sex of the user: 'male' or 'female'")

class BMRResponse(BaseModel):
    """Model representing a BMR calculation response."""
    bmr: float = Field(..., description="Calculated Basal Metabolic Rate (BMR)")

class TDEERequest(BaseModel):
    """Model representing a TDEE calculation request."""
    bmr: float = Field(..., description="Basal Metabolic Rate (BMR) of the user")
    activity_level: ActivityLevel = Field(..., description="Activity level of the user")

class TDEEResponse(BaseModel):
    """Model representing a TDEE calculation response."""
    tdee: float = Field(..., description="Calculated Total Daily Energy Expenditure (TDEE)")

class TargetCaloriesRequest(BaseModel):
    """Model representing a target daily caloric intake calculation request."""
    tdee: float = Field(..., description="Total Daily Energy Expenditure (TDEE) of the user")
    goal: Goal = Field(..., description="User's goal for caloric intake: 'lose weight', 'maintain weight', or 'gain weight'")

class TargetCaloriesResponse(BaseModel):
    """Model representing a target daily caloric intake calculation response."""
    target_calories: float = Field(..., description="Calculated target daily caloric intake")

class MacroNutrientRequest(BaseModel):
    """Model representing a macronutrient distribution calculation request."""
    target_calories: float = Field(..., description="Target daily caloric intake")
    goal: Goal = Field(..., description="User's goal for macronutrient distribution: 'lose weight', 'maintain weight', or 'gain weight'")

class MacroNutrientResponse(BaseModel):
    """Model representing a macronutrient distribution calculation response."""
    protein: float = Field(..., description="Calculated protein intake in grams")
    fat: float = Field(..., description="Calculated fat intake in grams")
    carbs: float = Field(..., description="Calculated carbohydrate intake in grams")

class IdealWeightRequest(BaseModel):
    """Model representing an ideal weight range calculation request."""
    height: float = Field(..., gt=0, description="Height of the user in centimeters or inches")
    sex: Sex = Field(..., description="Sex of the user: 'male' or 'female'")
    unit: UnitSystem = Field(..., description="Unit system for height: 'metric' or 'imperial'")

class IdealWeightResponse(BaseModel):
    """Model representing an ideal weight range calculation response."""
    ideal_weight_low: float = Field(..., description="Lower bound of the ideal weight range")
    ideal_weight_high: float = Field(..., description="Upper bound of the ideal weight range")


@tool
def calculate_bmr(request: BMRRequest) -> BMRResponse:
    """
    Calculate Basal Metabolic Rate (BMR) using the Mifflin-St Jeor Equation.

    Args:
        weight: Weight in kilograms (metric) or pounds (imperial).
        height: Height in centimeters (metric) or inches (imperial).
        age: Age in years.
        sex: 'male' or 'female'.
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
    return BMRResponse(bmr=round(bmr,1))

@tool
def calculate_bmi(request: BMIRequest) -> BMIResponse:
    """
    Calculate BMI and determine its category.

    Args:
        weight: Weight in kilograms (metric) or pounds (imperial).
        height: Height in meters (metric) or inches (imperial).
        unit: 'metric' or 'imperial'.

    Returns:
        BMI value and category.
    """
    if request.unit == UnitSystem.IMPERIAL:
        weight = _lbs_to_kg(request.weight)
        height = _inches_to_meters(request.height)
    else:
        weight = request.weight
        height = request.height
    bmi = weight / (height ** 2)
    category = _bmi_category(bmi)
    return BMIResponse(bmi=round(bmi,1), category=category)

def _bmi_category(bmi: float) -> str:
    """Determine the BMI category based on the BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity"
    
def _lbs_to_kg(pounds: float) -> float:
    """Convert weight from pounds to kilograms."""
    return pounds * 0.453592

def _inches_to_cm(inches: float) -> float:
    return inches * 2.54

def _inches_to_meters(inches: float) -> float:
    """Convert height from inches to meters."""
    return inches * 0.0254

@tool
def calculate_tdee(request: TDEERequest) -> TDEEResponse:
    """
    Calculate Total Daily Energy Expenditure (TDEE).

    Args:
        bmr: The Basal Metabolic Rate (BMR) of the user.
        activity_level: Activity level of the user.

    Returns:
        TDEE value.
    """
    tdee = request.bmr * request.activity_level.multiplier
    return TDEEResponse(tdee=round(tdee,1))

@tool
def calculate_target_calories(request: TargetCaloriesRequest) -> TargetCaloriesResponse:
    """
    Calculate target daily caloric intake based on TDEE and user goal.

    Args:
        tdee: Total Daily Energy Expenditure (TDEE).
        goal: User's goal - 'lose weight', 'maintain weight', or 'gain weight'.
    Returns:
        Target daily caloric intake.
    """
    if request.goal == Goal.LOSE_WEIGHT:
        target_calories = request.tdee - 500
    elif request.goal == Goal.GAIN_WEIGHT:
        target_calories = request.tdee + 500 
    else:
        target_calories = request.tdee
    return TargetCaloriesResponse(target_calories=round(target_calories,1))

@tool
def calculate_macros(request: MacroNutrientRequest) -> MacroNutrientResponse:
    """
    Calculate macronutrient distribution based on target calories and user goal.

    Args:
        target_calories: Target daily caloric intake.
        goal: User's goal - 'lose weight', 'maintain weight', or 'gain weight'.
    Returns:
        Macronutrient distribution in grams.
    """
    if request.goal == Goal.LOSE_WEIGHT:
        protein_ratio = 0.30
        fat_ratio = 0.25
        carb_ratio = 0.45
    elif request.goal == Goal.GAIN_WEIGHT:
        protein_ratio = 0.25
        fat_ratio = 0.30
        carb_ratio = 0.45
    else:  # maintain weight
        protein_ratio = 0.25
        fat_ratio = 0.30
        carb_ratio = 0.45

    protein_grams = (request.target_calories*protein_ratio) / 4
    fat_grams = (request.target_calories*fat_ratio) / 9
    carb_grams = (request.target_calories*carb_ratio) / 4

    return MacroNutrientResponse(protein=round(protein_grams,1), fat=round(fat_grams,1), carbs=round(carb_grams,1))

@tool
def calculate_ideal_weight(request: IdealWeightRequest) -> IdealWeightResponse:
    """
    Calculate ideal weight range based on height and gender.Devine foru
    
    """
    if request.sex == Sex.MALE:
        if request.unit == UnitSystem.IMPERIAL:
            ideal_weight_low = 106 + ((request.height - 60) * 6)
            ideal_weight_high = 126 + ((request.height - 60) * 6)
        else:
            ideal_weight_low = 45.5 + ((request.height - 152.4) * 0.9)
            ideal_weight_high = 55.5 + ((request.height - 152.4) * 0.9)
    else:
        if request.unit == UnitSystem.IMPERIAL:
            ideal_weight_low = 106 + ((request.height - 60) * 5)
            ideal_weight_high = 126 + ((request.height - 60) * 5)
        else:
            ideal_weight_low = 45.5 + ((request.height - 152.4) * 0.8)
            ideal_weight_high = 55.5 + ((request.height - 152.4) * 0.8)

    return IdealWeightResponse(ideal_weight_low=round(ideal_weight_low,1), ideal_weight_high=round(ideal_weight_high,1))