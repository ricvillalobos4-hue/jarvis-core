
import os
from anthropic import Anthropic

from core.personality import (
    JARVIS_SYSTEM_PROMPT
)


class JarvisBrain:

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise RuntimeError(
                "JARVIS necesita configurar su API key."
            )

        self.client = Anthropic(api_key=api_key)

        self.model = os.getenv(
            "ANTHROPIC_MODEL",
            "claude-sonnet-4-5"
        )

        self.history = []

    def think(self, message):

        if not isinstance(message, str) or not message.strip():
            raise ValueError("El mensaje no puede estar vacío.")

        self.history.append({
            "role": "user",
            "content": message.strip()
        })

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=JARVIS_SYSTEM_PROMPT,
            messages=self.history[-20:]
        )

        answer = "".join(
            block.text
            for block in response.content
            if block.type == "text"
        )

        self.history.append({
            "role": "assistant",
            "content": answer
        })

        return answer
