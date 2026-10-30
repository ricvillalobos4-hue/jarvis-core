
import os
from anthropic import Anthropic

from core.personality import JARVIS_SYSTEM_PROMPT
from core.memory import JarvisMemory


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
        self.memory = JarvisMemory()

    def remember(self, information):
        return self.memory.remember(information)

    def recall(self):
        return self.memory.recall()

    def forget_all_memories(self):
        return self.memory.forget_all()

    def think(self, message):

        if not isinstance(message, str) or not message.strip():
            raise ValueError("El mensaje no puede estar vacío.")

        self.history.append({
            "role": "user",
            "content": message.strip()
        })

        saved_memories = self.memory.recall()

        memory_context = "\n".join(
            f"- {item['information']}"
            for item in saved_memories
        )

        system_prompt = JARVIS_SYSTEM_PROMPT

        if memory_context:
            system_prompt += (
                "\n\nMEMORIA PERSISTENTE DE JARVIS:\n"
                + memory_context
                + "\nUtiliza estos recuerdos cuando sean relevantes."
            )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt,
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
