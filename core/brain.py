import os
from anthropic import Anthropic
from core.personality import get_system_prompt
from core.memory import JarvisMemory
from core.tools import execute_tool

class JarvisBrain:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Falta la variable de entorno ANTHROPIC_API_KEY.")
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.memory = JarvisMemory()

    def process_message(self, user_message: str) -> str:
        try:
            self.memory.add_message("user", user_message)
            tool_response = None
            msg_lower = user_message.lower()

            if "hora" in msg_lower:
                tool_response = execute_tool("get_time")
            elif "estado" in msg_lower or "sistema" in msg_lower:
                tool_response = execute_tool("system_status")

            if tool_response:
                system_content = f"{get_system_prompt()}\n\nInformación del sistema: {tool_response}"
            else:
                system_content = get_system_prompt()

            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_content,
                messages=self.memory.get_history()
            )

            assistant_reply = response.content[0].text
            self.memory.add_message("assistant", assistant_reply)
            return assistant_reply
        except Exception as e:
            return f"Error en el núcleo de JARVIS: {str(e)}"
