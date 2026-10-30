class JarvisMemory:
    def __init__(self):
        # Memoria en curso simple para mantener el contexto
        self.history = []

    def add_message(self, role: str, content: str):
        """Agrega un mensaje al historial de la conversación."""
        self.history.append({"role": role, "content": content})
        # Mantener un límite de 20 mensajes para no exceder los tokens de la API
        if len(self.history) > 20:
            self.history = self.history[-20:]

    def get_history(self) -> list:
        """Devuelve el historial actual de mensajes."""
        return self.history

    def clear(self):
        """Limpia la memoria actual."""
        self.history = []
