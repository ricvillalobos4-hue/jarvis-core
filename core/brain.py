
import os
from anthropic import Anthropic


JARVIS_IDENTITY = """
Tu nombre es JARVIS.
Tu usuario principal es Kerens.

Eres un asistente personal inteligente,
elegante, sereno y profesional.

Hablas español naturalmente.

Tu misión es ayudar a Kerens a:
- Razonar y analizar problemas.
- Investigar información.
- Planificar proyectos.
- Resolver problemas.
- Programar y aprender.

REGLAS:
- Siempre llama al usuario Kerens.
- Nunca lo llames Tony Stark ni Señor Stark.
- No inventes información ni recuerdos.
- Reconoce tus limitaciones.
- Solicita autorización antes de ejecutar
  acciones externas.
- Nunca afirmes haber realizado acciones
  que no hayas ejecutado.

Tu memoria y herramientas externas estarán
disponibles cuando se conecten sus módulos.
"""


class JarvisBrain:

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise RuntimeError(
                "Falta configurar ANTHROPIC_API_KEY"
            )

        self.client = Anthropic(api_key=api_key)

        self.model = os.getenv(
            "ANTHROPIC_MODEL",
            "claude-sonnet-5-5"
        )

        self.history = []

    def think(self, message):

        if not message.strip():
            raise ValueError("Mensaje vacío.")

        self.history.append({
            "role": "user",
            "content": message
        })

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1200,
            system=JARVIS_IDENTITY,
            messages=self.history
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
