class JarvisTools:
    def __init__(self):
        self.commands = {
            "hora": self.get_time,
            "estado": self.get_status,
        }

    def get_time(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M")

    def get_status(self):
        return "JARVIS CORE está operativo."

    def execute(self, command):
        if not isinstance(command, str):
            return "Comando no válido."

        command = command.lower().strip()
        action = self.commands.get(command)

        if action is None:
            return "No reconozco ese comando."

        return action()
