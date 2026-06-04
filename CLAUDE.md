# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es este proyecto

Repositorio de aprendizaje y experimentación del **Google ADK** (Agent Development Kit, paquete `google-adk`). Define agentes LLM que corren sobre modelos Gemini.

## Entorno y comandos

El proyecto usa **`uv`** para gestión de dependencias (Python `>=3.12`, fijado a 3.12 en `.python-version`).

```bash
uv sync                 # Instalar/sincronizar dependencias desde uv.lock
uv add <paquete>        # Añadir una dependencia (actualiza pyproject.toml + uv.lock)
uv run adk web          # UI web de desarrollo del ADK (descubre agentes en subdirectorios)
uv run adk run my_agent # Ejecutar un agente en consola
```

`adk web` / `adk run` descubren agentes buscando paquetes que exporten `root_agent` (ver convención abajo). Ejecuta los comandos desde la raíz del repo, no desde dentro de `my_agent/`.

## Convención de estructura de un agente (ADK)

Cada agente es un **paquete de Python** (directorio con `__init__.py`), no un módulo suelto. El ADK lo descubre por esta convención exacta:

- `<agente>/__init__.py` → debe hacer `from . import agent` para que el ADK cargue el módulo.
- `<agente>/agent.py` → debe exponer una variable de nivel de módulo llamada **`root_agent`** (un `Agent` del ADK). El descubrimiento del ADK busca este nombre específicamente; renombrarla rompe `adk web`/`adk run`.
- `<agente>/.env` → credenciales por agente (cargado automáticamente por el ADK). No se commitea (`.gitignore`).

El agente de ejemplo está en [my_agent/agent.py](my_agent/agent.py).

## Configuración de credenciales

El `.env` de cada agente define cómo se autentica contra Gemini:

- `GOOGLE_GENAI_USE_VERTEXAI` → `FALSE` usa la API de Gemini con API key; `TRUE` usa Vertex AI (requiere proyecto/región de GCP en su lugar).
- `GOOGLE_API_KEY` → API key de Google AI Studio (solo cuando `USE_VERTEXAI=FALSE`).

## Notas

- `my_agent/.adk/session.db` es estado de sesión generado en runtime por `adk web` (SQLite). No es código fuente; no editarlo a mano.
