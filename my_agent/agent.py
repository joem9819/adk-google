from datetime import datetime

from google.adk.agents.llm_agent import Agent


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {
        "status": "success",
        "city": city,
        "time": datetime.now().strftime("%I:%M %p"),
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Indica la hora actual en una ciudad determinada.",
    instruction="Eres un asistente útil que indica la hora actual en las ciudades. Usa la herramienta 'get_current_time' para este propósito.",
    tools=[get_current_time],
)