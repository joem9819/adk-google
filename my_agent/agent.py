from datetime import datetime
from typing import Optional, Dict, Any

from google.adk.agents.llm_agent import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {
        "status": "success",
        "city": city,
        "time": datetime.now().strftime("%I:%M %p"),
    }


# Conjunto de palabras ofensivas; usar set en lugar de lista hace la búsqueda O(1)
PALABRAS_INSULTO = {
    "idiota", "estupido", "imbecil", "maldito", "inutil",
    "tonto", "basura", "idiot", "stupid", "dumb", "moron","hijuputa", "pendejo", "gilipollas", "cabrón", "zorra", "puta"
    "malparido", "gonorrea"
}

def block_keyword_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Bloquea la llamada al LLM si el mensaje contiene insultos."""
    last_user_message = ""
    if llm_request.contents:
        # Recorremos el historial al revés para encontrar el último mensaje del usuario
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts:
                if content.parts[0].text:
                    last_user_message = content.parts[0].text
                    break

    # Dividimos en palabras individuales para evitar falsos positivos por subcadenas
    palabras_mensaje = last_user_message.lower().split()

    # next() devuelve el primer insulto encontrado, o None si no hay ninguno
    insulto_encontrado = next(
        (p for p in palabras_mensaje if p in PALABRAS_INSULTO), None
    )

    if insulto_encontrado:
        # Guardamos en el estado de sesión para auditoría o trazabilidad posterior
        callback_context.state["guardrail_block_triggered"] = True
        callback_context.state["guardrail_block_word"] = insulto_encontrado

        # Retornar LlmResponse hace que ADK use esta respuesta y NO llame al LLM
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="Por favor, mantén un tono respetuoso. No puedo responder a mensajes con lenguaje ofensivo.")],
            )
        )
    # Retornar None indica a ADK que continúe con la llamada al LLM normalmente
    return None


def block_city_tool_guardrail(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    """Bloquea get_current_time si la ciudad es 'Moscú'."""
    if tool.name == "get_current_time":
        # Obtenemos el argumento 'city' que el LLM decidió pasar a la herramienta
        city = args.get("city", "")

        # Comparamos en minúsculas para que no importe cómo escribió el LLM la ciudad
        if city.lower() == "moscú" or city.lower() == "moscow":
            tool_context.state["guardrail_tool_block_triggered"] = True

            # Retornar un dict hace que ADK lo use como resultado de la tool sin ejecutarla
            return {
                "status": "error",
                "error_message": f"Restricción de política: la consulta de hora para '{city}' está deshabilitada.",
            }
    # Retornar None permite que la herramienta se ejecute con normalidad
    return None


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Indica la hora actual en una ciudad determinada.",
    instruction="Eres un asistente útil que indica la hora actual en las ciudades. Usa la herramienta 'get_current_time' para este propósito.",
    tools=[get_current_time],
    # Se ejecuta justo antes de enviar la petición al LLM
    before_model_callback=block_keyword_guardrail,
    # Se ejecuta justo antes de que una herramienta sea invocada
    before_tool_callback=block_city_tool_guardrail,
)