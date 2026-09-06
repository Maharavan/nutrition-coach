"""Nutritions module for handling nutritional data and calculations."""

from strands import tool, ToolContext

from services.llm_service import llm_service
from services.tavily_service import tavily_service
from tools.models import (
    FoodNutritionRequest,
    FoodSwapRequest,
    FoodSwapResponse,
    MealAnalysisRequest,
    MealAnalysisResponse,
    MealPlanRequest,
    MealPlanResponse,
    NutritionInfoResponse,
    NutritionResearchRequest,
    NutritionResearchResponse,
    RecipeRequest,
    RecipeResponse,
)

# --------------------------------------------------------------------------
# Tools
# --------------------------------------------------------------------------


@tool(context=True)
def lookup_food_nutrition(request: FoodNutritionRequest, tool_context: ToolContext) -> NutritionInfoResponse:
    """Retrieve nutritional information for a food."""
    search_response = tavily_service.search(query=f"Nutritional information for {request.food_name}")
    context = search_response.results
    if not context:
        return NutritionInfoResponse(
            food_name=request.food_name,
            info="No reliable nutritional information was found."
        )

    system_prompt = (
        "You are a nutrition expert. Provide accurate nutritional "
        "information including calories, protein, carbohydrates, fat, "
        "fiber, and important micronutrients."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=context)
    return NutritionInfoResponse(food_name=request.food_name, info=response.content)


@tool(context=True)
def analyze_meal(request: MealAnalysisRequest, tool_context: ToolContext) -> MealAnalysisResponse:
    """Analyze a meal and provide nutritional feedback."""
    system_prompt = (
        "You are a nutrition expert. Analyze the meal, estimate calories "
        "and macronutrients, identify strengths and weaknesses, and "
        "suggest practical improvements."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=request.meal)
    return MealAnalysisResponse(analysis=response.content)


@tool(context=True)
def generate_meal_plan(request: MealPlanRequest, tool_context: ToolContext) -> MealPlanResponse:
    """Generate a personalized meal plan."""
    system_prompt = (
        "You are a registered dietitian. Generate a personalized meal "
        "plan based on the user's goals, calorie target, dietary "
        "preferences, allergies, and lifestyle."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=request.requirements)
    return MealPlanResponse(meal_plan=response.content)


@tool(context=True)
def recommend_recipe(request: RecipeRequest, tool_context: ToolContext) -> RecipeResponse:
    """Generate a healthy recipe."""
    system_prompt = (
        "You are a healthy recipe assistant. Create a nutritious recipe "
        "with ingredients, preparation steps, and estimated nutrition."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=request.request)
    return RecipeResponse(recipe=response.content)


@tool(context=True)
def recommend_food_swap(request: FoodSwapRequest, tool_context: ToolContext) -> FoodSwapResponse:
    """Recommend healthier alternatives for a food."""
    system_prompt = (
        "You are a nutrition coach. Recommend healthier alternatives "
        "while keeping similar taste, convenience, and nutritional value."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=request.food)
    return FoodSwapResponse(suggestions=response.content)


@tool(context=True)
def nutrition_research(request: NutritionResearchRequest, tool_context: ToolContext) -> NutritionResearchResponse:
    """Answer nutrition questions using web research."""
    search_response = tavily_service.search(request.question)

    if search_response.results:
        user_prompt = (
            f"Question: {request.question}\n\n"
            f"Use the following research to answer:\n\n{search_response.results}"
        )
    else:
        user_prompt = request.question

    system_prompt = (
        "You are a nutrition research assistant. Answer using reliable "
        "scientific evidence and summarize the key findings clearly. "
        "Cite sources from the provided research where relevant."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=user_prompt)
    return NutritionResearchResponse(answer=response.content)
