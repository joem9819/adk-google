# adk-google
Repositorio para desarrollo y aprendizaje del adk de google

## Comandos

### Crear un agente

```bash
adk create my_agent
```

Genera el paquete del agente (`my_agent/`). De forma interactiva pide
seleccionar el **modelo** (queda en `my_agent/agent.py`) y la **API key**
(queda en `my_agent/.env`).

### Levantar la UI web de desarrollo

```bash
adk web
```

Inicia la interfaz web del ADK para conversar con el agente. Ejecútalo desde
la raíz del repo; descubre los agentes en los subdirectorios.

### Ejecutar un agente en consola

```bash
adk run my_agent
```

Inicia una sesión de chat con el agente directamente en la terminal, sin la UI
web. Ejecútalo desde la raíz del repo.
