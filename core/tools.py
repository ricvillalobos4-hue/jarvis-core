from datetime import datetime
import platform

def execute_tool(tool_name: str, args: dict = None) -> str:
    """Ejecuta una herramienta específica según el comando solicitado."""
    if tool_name == "get_time":
        now = datetime.now()
        return f"La hora actual del sistema es: {now.strftime('%H:%M:%S')} del {now.strftime('%d/%m/%Y')}."
    
    elif tool_name == "system_status":
        return f"Sistemas operativos estables. Entorno: {platform.system()} {platform.release()}. Servidor en línea."
    
    return f"Herramienta '{tool_name}' no reconocida."
