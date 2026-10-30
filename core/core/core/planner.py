
class JarvisPlanner:

    def create_plan(self, objective):

        if not objective or not objective.strip():
            raise ValueError("Objetivo vacío.")

        return {
            "assistant": "JARVIS",
            "user": "Kerens",
            "objective": objective.strip(),
            "status": "pending_analysis",
            "instructions": [
                "Comprender el objetivo.",
                "Identificar los requisitos.",
                "Dividir el objetivo en tareas.",
                "Evaluar riesgos y dependencias.",
                "Presentar el plan a Kerens.",
                "Esperar autorización antes de actuar."
            ],
            "requires_approval": True
        }
