"""Health research tools."""

from strands import tool, ToolContext

from services.llm_service import llm_service
from services.tavily_service import tavily_service
from tools.models import (
    FactCheckRequest,
    FactCheckResponse,
    HealthResearchRequest,
    HealthResearchResponse,
)

# --------------------------------------------------------------------------
# Tools
# --------------------------------------------------------------------------


@tool(context=True)
def health_research(request: HealthResearchRequest, tool_context: ToolContext) -> HealthResearchResponse:
    """Answer health questions using web research."""
    search_response = tavily_service.search(request.question)

    if search_response.results:
        user_prompt = (
            f"Question: {request.question}\n\n"
            f"Use the following research to answer:\n\n{search_response.results}"
        )
    else:
        user_prompt = request.question

    system_prompt = (
        "You are a health research assistant. Answer using reliable "
        "medical and scientific evidence, and summarize the key findings "
        "clearly. Cite sources from the provided research where relevant. "
        "Recommend consulting a healthcare professional for personal "
        "medical decisions."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=user_prompt)
    return HealthResearchResponse(answer=response.content)


@tool(context=True)
def fact_check_health_claim(request: FactCheckRequest, tool_context: ToolContext) -> FactCheckResponse:
    """Fact-check a health claim using web research."""
    search_response = tavily_service.search(f"fact check: {request.claim}")

    if search_response.results:
        user_prompt = (
            f"Claim: {request.claim}\n\n"
            f"Use the following research to fact-check this claim:\n\n{search_response.results}"
        )
    else:
        user_prompt = f"Claim: {request.claim}"

    system_prompt = (
        "You are a health fact-checking assistant. Evaluate the claim "
        "using reliable medical and scientific evidence. State a clear "
        "verdict (True, False, Misleading, or Unverified), explain your "
        "reasoning, and cite sources from the provided research where "
        "relevant."
    )

    response = llm_service.generate(system_prompt=system_prompt, user_prompt=user_prompt)
    return FactCheckResponse(verdict=response.content)
