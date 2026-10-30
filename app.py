import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from core.brain import JarvisBrain

load_dotenv()

app = Flask(__name__)

jarvis = None


def get_jarvis():
    global jarvis

    if jarvis is None:
        jarvis = JarvisBrain()

    return jarvis


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "name": "JARVIS CORE",
        "status": "online",
        "message": "JARVIS está listo."
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "operational"
    })


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message", "")

        if not isinstance(message, str) or not message.strip():
            return jsonify({
                "error": "Escribe un mensaje válido."
            }), 400

        response = get_jarvis().think(message)

        return jsonify({
            "assistant": "JARVIS",
            "response": response
        })

    except Exception as error:
        app.logger.exception("Error en JARVIS")

        return jsonify({
            "error": "JARVIS encontró un problema.",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=False
    )
