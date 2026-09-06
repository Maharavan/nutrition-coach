# AI Nutrition Coach

An intelligent AI-powered nutrition coaching application built with FastAPI and Strands Agents framework.

## Features

### 🎯 Core Capabilities
- **Personalized Nutrition Advice** - Get evidence-based nutrition recommendations using AI
- **Body Metrics Calculations** - BMI, BMR, TDEE, macronutrient distribution
- **Exercise Recommendations** - Personalized workout plans and exercise suggestions
- **Meal Planning** - AI-generated meal plans tailored to your goals
- **Health Research** - Real-time web search integration for nutrition facts
- **Daily Motivation** - Personalized motivational messages and habit tips
- **Persistent Memory** - User profiles and preferences stored for personalized experiences

### 🛠 Technical Stack
- **FastAPI** - Modern Python web framework
- **Strands Agents** - Multi-agent orchestration framework
- **OpenAI GPT-4** - Large language model for intelligent responses
- **Tavily** - Real-time web search API
- **Mem0** - Persistent memory management
- **Pydantic** - Data validation and settings management

## Setup

### Prerequisites
- Python 3.10+
- pip or uv (package manager)
- API keys for: OpenAI, Tavily, and Mem0

### Installation

1. **Clone and navigate to project:**
```bash
cd dont-know
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run the application:**
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Chat Endpoint
**POST** `/chat`

Send a message to the nutrition coach and get personalized advice.

**Request:**
```json
{
  "user_id": 1,
  "message": "What should I eat to lose weight?",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Response:**
```json
{
  "response": "Based on your goals, here are my recommendations...",
  "timestamp": "2024-01-01T12:00:01Z"
}
```

## Available Tools

The nutrition coach has access to 20 specialized tools:

### Body Metrics (6 tools)
- `calculate_bmi` - Calculate Body Mass Index
- `calculate_bmr` - Calculate Basal Metabolic Rate
- `calculate_tdee` - Calculate Total Daily Energy Expenditure
- `calculate_target_calories` - Calculate caloric needs for goals
- `calculate_macros` - Calculate macronutrient distribution
- `calculate_ideal_weight` - Calculate ideal body weight

### Exercise (4 tools)
- `estimate_calories_burned` - Estimate calories burned during activities
- `recommend_workout` - Generate personalized workout plans
- `recommend_exercise` - Suggest specific exercises
- `recommend_recovery_plan` - Create post-workout recovery plans

### Nutrition (6 tools)
- `lookup_food_nutrition` - Get nutritional information for foods
- `analyze_meal` - Analyze meals for nutritional content
- `generate_meal_plan` - Create personalized meal plans
- `recommend_recipe` - Suggest healthy recipes
- `recommend_food_swap` - Recommend healthier food alternatives
- `nutrition_research` - Research nutrition topics

### Health Research (2 tools)
- `health_research` - Research health questions using web search
- `fact_check_health_claim` - Verify health claims with evidence

### Motivation (2 tools)
- `daily_motivation` - Get daily motivational messages
- `healthy_habit_tip` - Get actionable health tips

## Logging

Logs are automatically configured and saved to the `logs/` directory:
- **Console output** - INFO level and above
- **File output** - DEBUG level and above (rotating, max 10MB)

View logs:
```bash
tail -f logs/nutrition_coach.log
```

## Project Structure

```
.
├── app.py                          # FastAPI application
├── config.py                       # Configuration and settings
├── logger_config.py               # Logging configuration
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
│
├── agent/
│   ├── nutrition_agent.py         # Main nutrition agent
│   └── agent_prompt.md            # Agent system prompt
│
├── api/
│   ├── router.py                  # API endpoints
│   └── models.py                  # Request/response models
│
├── services/
│   ├── llm_service.py             # LLM integration
│   └── tavily_service.py          # Web search integration
│
└── tools/
    ├── body_metrics_tools.py      # Calculation tools
    ├── exercise_tools.py          # Workout tools
    ├── nutrition_tools.py         # Nutrition tools
    ├── research_tools.py          # Research tools
    ├── motivation_tools.py        # Motivation tools
    ├── constants.py               # Enums and constants
    └── models.py                  # Pydantic models
```

## Environment Variables

### Required
- `API_KEY` - OpenAI API key
- `MEM0_API_KEY` - Mem0 API key for persistent memory
- `TAVILY_API_KEY` - Tavily API key for web search

### Optional
- `AGENT_MODEL_NAME` - Primary LLM (default: gpt-4o)
- `AGENT_FALLBACK_MODEL_NAME` - Fallback LLM (default: gpt-4o-mini)
- `AGENT_MAX_TOKENS` - Max response tokens (default: 4096)
- `AGENT_TEMPERATURE` - Response creativity (default: 0.3)

See `.env.example` for all options.

## Development

### Run Tests (when implemented)
```bash
pytest tests/
```

### Lint Code
```bash
pylint app.py config.py
```

### Format Code
```bash
black .
```

## Troubleshooting

### Import Error: "partially initialized module 'logging'"
**Solution:** Make sure there's no `logging.py` file in the project root. Use `logger_config.py` instead.

### API Keys Not Found
**Solution:** Ensure `.env` file exists in the project root with valid API keys.

### Agent Not Finding Tools
**Solution:** Run validation to verify tool discovery:
```bash
python validate_tools.py
```

## Contributing

1. Follow the existing code structure
2. Use proper logging with `logger = logging.getLogger(__name__)`
3. Add type hints to all functions
4. Test changes before committing

## License

MIT License

## Support

For issues and questions, please refer to:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Strands Agents Docs](https://github.com/strands-ai/strands)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
