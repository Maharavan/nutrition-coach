from strands import tool, ToolContext

from services.llm_service import llm_service
from tools.body_metrics_tools import _lbs_to_kg
from tools.constants import UnitSystem
from tools.models import (
    CaloriesBurnedRequest,
    CaloriesBurnedResponse,
    ExerciseRecommendationRequest,
    ExerciseRecommendationResponse,
    RecoveryPlanRequest,
    RecoveryPlanResponse,
    WorkoutRequest,
    WorkoutResponse,
)


@tool(context=True)
def estimate_calories_burned(request: CaloriesBurnedRequest, tool_context: ToolContext) -> CaloriesBurnedResponse:
    """
    Estimate calories burned during an activity using the MET formula.

    Args:
        request: Weight, unit system, activity duration, and exercise type.

    Returns:
        The estimated calories burned.
    """
    weight = _lbs_to_kg(request.weight) if request.unit == UnitSystem.IMPERIAL else request.weight
    calories_burned = request.exercise_type.met * weight * (request.duration_minutes / 60)

    return CaloriesBurnedResponse(calories_burned=round(calories_burned, 1))

@tool(context=True)
def recommend_workout(request: WorkoutRequest, tool_context: ToolContext) -> WorkoutResponse:
    """Generate a personalized workout recommendation."""
    system_prompt = (
        "You are a certified fitness coach. Design a workout based on the "
        "user's goals, available equipment, time constraints, and "
        "experience level."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=request.requirements)
    return WorkoutResponse(workout_plan=response.content)


@tool(context=True)
def recommend_exercise(
    request: ExerciseRecommendationRequest, tool_context: ToolContext
) -> ExerciseRecommendationResponse:
    """Recommend an exercise for a target muscle group or goal."""
    system_prompt = (
        "You are a certified fitness coach. Recommend a suitable exercise "
        "including proper form, recommended sets and reps, and common "
        "mistakes to avoid."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=request.query)
    return ExerciseRecommendationResponse(recommendation=response.content)


@tool(context=True)
def recommend_recovery_plan(request: RecoveryPlanRequest, tool_context: ToolContext) -> RecoveryPlanResponse:
    """Generate a personalized post-workout recovery plan."""
    system_prompt = (
        "You are a sports recovery specialist. Based on the workout "
        "performed, soreness, injuries, or fatigue level described, "
        "recommend a recovery plan covering rest, stretching, mobility "
        "work, and nutrition."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=request.details)
    return RecoveryPlanResponse(recovery_plan=response.content)