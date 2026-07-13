"""Nutritions module for handling nutritional data and calculations."""

from strands import tool

from services.llm_service import llm_service
from services.tavily_service import tavily_service, SearchResult
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


def _build_search_context(results: list[SearchResult]) -> str:
    """Build a formatted context string from search results.
    
    Args:
        results: List of search results to format.
        
    Returns:
        Formatted string combining all search results.
    """
    return "\n\n".join(
        f"Source: {result.title}\n"
        f"URL: {result.url}\n"
        f"{result.content}"
        for result in results
    )

# --------------------------------------------------------------------------
# Tools
# --------------------------------------------------------------------------


@tool
def lookup_food_nutrition(request: FoodNutritionRequest) -> NutritionInfoResponse:
    """Retrieve nutritional information for a food."""
    search_response = tavily_service.search(query=f"Nutritional information for {request.food_name}")
    results = search_response.results or []
    if not results:
        return NutritionInfoResponse(
            food_name=request.food_name,
            info="No reliable nutritional information was found."
        )

    context = _build_search_context(results)

    system_prompt = (
        "You are a nutrition expert. Provide accurate nutritional "
        "information including calories, protein, carbohydrates, fat, "
        "fiber, and important micronutrients."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=context)
    return NutritionInfoResponse(food_name=request.food_name, info=response.content)


@tool
def analyze_meal(request: MealAnalysisRequest) -> MealAnalysisResponse:
    """Analyze a meal and provide nutritional feedback."""
    system_prompt = (
        "You are a nutrition expert. Analyze the meal, estimate calories "
        "and macronutrients, identify strengths and weaknesses, and "
        "suggest practical improvements."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=request.meal)
    return MealAnalysisResponse(analysis=response.content)


@tool
def generate_meal_plan(request: MealPlanRequest) -> MealPlanResponse:
    """Generate a personalized meal plan."""
    system_prompt = (
        "You are a registered dietitian. Generate a personalized meal "
        "plan based on the user's goals, calorie target, dietary "
        "preferences, allergies, and lifestyle."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=request.requirements)
    return MealPlanResponse(meal_plan=response.content)


@tool
def recommend_recipe(request: RecipeRequest) -> RecipeResponse:
    """Generate a healthy recipe."""
    system_prompt = (
        "You are a healthy recipe assistant. Create a nutritious recipe "
        "with ingredients, preparation steps, and estimated nutrition."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=request.request)
    return RecipeResponse(recipe=response.content)


@tool
def recommend_food_swap(request: FoodSwapRequest) -> FoodSwapResponse:
    """Recommend healthier alternatives for a food."""
    system_prompt = (
        "You are a nutrition coach. Recommend healthier alternatives "
        "while keeping similar taste, convenience, and nutritional value."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=request.food)
    return FoodSwapResponse(suggestions=response.content)


@tool
def nutrition_research(request: NutritionResearchRequest) -> NutritionResearchResponse:
    """Answer nutrition questions using web research."""
    search_response = tavily_service.search(request.question)

    results = search_response.results or []
    if results:
        research_context = _build_search_context(results=results)
        user_prompt = (
            f"Question: {request.question}\n\n"
            f"Use the following research to answer:\n\n{research_context}"
        )
    else:
        user_prompt = request.question

    system_prompt = (
        "You are a nutrition research assistant. Answer using reliable "
        "scientific evidence and summarize the key findings clearly. "
        "Cite sources from the provided research where relevant."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=user_prompt)
    return NutritionResearchResponse(answer=response.content, sources=results)
