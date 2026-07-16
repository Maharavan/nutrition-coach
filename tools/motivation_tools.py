"""Motivation tools."""

from strands import tool, ToolContext

from services.llm_service import llm_service
from tools.models import (
    HealthyHabitTipRequest,
    HealthyHabitTipResponse,
    MotivationRequest,
    MotivationResponse,
)

# --------------------------------------------------------------------------
# Tools
# --------------------------------------------------------------------------


@tool(context=True)
def daily_motivation(request: MotivationRequest, tool_context: ToolContext) -> MotivationResponse:
    """Generate a short daily motivational message for health and fitness goals."""
    system_prompt = (
        "You are an encouraging health and fitness coach. Write a short, "
        "uplifting daily motivational message that inspires the user to "
        "stay consistent with their health and fitness goals. Keep it "
        "positive, genuine, and free of clichés."
    )

    user_prompt = (
        f"Context about the user: {request.context}"
        if request.context
        else "Write a general daily motivational message for someone working on their health and fitness."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=user_prompt)
    return MotivationResponse(message=response.content)


@tool(context=True)
def healthy_habit_tip(request: HealthyHabitTipRequest, tool_context: ToolContext) -> HealthyHabitTipResponse:
    """Generate a practical, actionable healthy habit tip."""
    system_prompt = (
        "You are a health and wellness coach. Share one practical, "
        "actionable healthy habit tip that is easy to apply today. Keep "
        "it concise and evidence-based."
    )

    user_prompt = (
        f"Focus area: {request.category}"
        if request.category
        else "Share a healthy habit tip covering any area of general wellness."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=user_prompt)
    return HealthyHabitTipResponse(tip=response.content)
