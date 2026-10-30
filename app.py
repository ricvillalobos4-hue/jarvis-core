import os
from flask import Flask, request, jsonify
from core.brain import JarvisBrain

app = Flask(__name__)

jarvis = None

def get_jarvis():
    global jarvis
    if jarvis is None:
        jarvis = JarvisBrain()
    return jarvis

@app.route("/", methods=["GET"])
def home():
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JARVIS CORE</title>
<style>
body { background: #0f172a; color: #f8fafc; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
.card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; width: 100%; max-width: 500px; padding: 20px; box-sizing: border-box; }
h1 { color: #38bdf8; margin: 0 0 10px 0; font-size: 1.4rem; text-align: center; }
.status { color: #4ade80; text-align: center; font-size: 0.85rem; margin-bottom: 15px; }
#chat { height: 320px; overflow-y: auto; background: #0b0f19; border-radius: 8px; padding: 12px; display: flex; flex-direction: column; gap: 8px; margin-bottom: 15px; }
.msg { padding: 8px 12px; border-radius: 8px; font-size: 0.9rem; max-width: 80%; line-height: 1.4; }
.user { background: #0284c7; color: white; align-self: flex-end; }
.jarvis { background: #334155; color: #e2e8f0; align-self: flex-start; }
.input-row { display: flex; gap: 8px; }
input { flex: 1; padding: 10px; border-radius: 8px; border: 1px solid #334155; background: #0b0f19; color: white; font-size: 0.95rem; outline: none; }
button { background: #0284c7; color: white; border: none; border-radius: 8px; padding: 0 16px; font-weight: bold; cursor: pointer; }
</style>
</head>
<body>
<div class="card">
<h1>JARVIS CORE 🤖</h1>
<div class="status">● Sistema en línea</div>
<div id="chat">
<div class="msg jarvis">Sistemas listos. ¿En qué puedo ayudarte?</div>
</div>
<div class="input-row">
<input type="text" id="text" placeholder="Escribe un mensaje..." onkeypress="if(event.key==='Enter')send()">
<button onclick="send()">Enviar</button>
</div>
</div>
<script>
async function send() {
const el = document.getElementById('text');
const val = el.value.trim();
if (!val) return;
const chat = document.getElementById('chat');
chat.innerHTML += `<div class="msg user">${val}</div>`;
el.value = '';
chat.scrollTop = chat.scrollHeight;
try {
const res = await fetch('/chat', {
method: 'POST',
headers: {'Content-Type': 'application/json'},
body: JSON.stringify({message: val})
});
const data = await res.json();
chat.innerHTML += `<div class="msg jarvis">${data.reply || data.error}</div>`;
} catch (e) {
chat.innerHTML += `<div class="msg jarvis">Error de comunicación.</div>`;
}
chat.scrollTop = chat.scrollHeight;
}
</script>
</body>
</html>"""

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "system": "JARVIS CORE online"}), 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Mensaje vacío"}), 400
    try:
        instance = get_jarvis()
        reply = instance.process_message(message)
        return jsonify({"reply": reply}), 200
    except Exception as e:
        return jsonify({"error": f"Error en JARVIS: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
