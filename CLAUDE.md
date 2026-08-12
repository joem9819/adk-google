# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es este proyecto

Repositorio de aprendizaje y experimentación del **Google ADK** (Agent Development Kit, paquete `google-adk`). Define agentes LLM que corren sobre modelos Gemini.

## Fuentes de verdad sobre el ADK (verificar antes de responder)

El ADK evoluciona rápido y la versión instalada puede ser **posterior a la fecha de corte de conocimiento del modelo**. Por eso: **no respondas de memoria sobre la API del ADK** —clases, firmas, parámetros, módulos disponibles, features nuevas—. Verificá siempre en una de las dos fuentes de abajo antes de afirmar algo o escribir código, y citá de dónde salió.

### 1. Código instalado → qué existe y qué firma tiene

```
.venv/Lib/site-packages/google/adk/
```

Fuente autoritativa para preguntas de API concretas: si una clase existe, qué parámetros acepta un callback, qué exporta un submódulo. Corresponde **exactamente a la versión que ejecuta este proyecto**, a diferencia de `main` en GitHub, que suele ir más adelantado. Leerlo/grepearlo con Read y Grep; no hace falta clonar el repo.

- Versión instalada: [.venv/Lib/site-packages/google/adk/version.py](.venv/Lib/site-packages/google/adk/version.py)
- Submódulos: `agents/`, `tools/`, `models/`, `flows/`, `sessions/`, `memory/`, `plugins/`, `events/`, `artifacts/`, `auth/`, `planners/`, `code_executors/`, `evaluation/`, `skills/`, `workflow/`, `apps/`, `a2a/`, `cli/`, entre otros (29 en total).

### 2. Documentación oficial → por qué, cuándo y con qué patrón

Consultarla (WebFetch) para conceptos, guías, buenas prácticas y novedades: el código da la firma, pero no el criterio de diseño ni el patrón recomendado.

| Recurso | URL |
|---|---|
| Documentación | https://google.github.io/adk-docs/ |
| Repositorio | https://github.com/google/adk-python |
| Changelog | https://github.com/google/adk-python/blob/main/CHANGELOG.md |
| Paquete en PyPI | https://pypi.org/project/google-adk/ |

Ante una discrepancia entre la documentación y el código instalado, **gana el código instalado**: es lo que realmente corre acá.

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
