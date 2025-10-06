from flask import Flask, render_template, request, jsonify
import requests
from personas import personas

app = Flask(__name__)

OLLAMA_API = "http://localhost:11434/api/generate"

@app.route("/")
def home():
    return render_template("index.html", personas=personas)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    persona_key = data.get("persona")
    user_input = data.get("message")

    prompt = f"{personas[persona_key]['style']}\nUser: {user_input}\nAssistant:"
    
    response = requests.post(OLLAMA_API, json={
        "model": "phi3:mini",
        "prompt": prompt
    }, stream=True)

    reply = ""
    for line in response.iter_lines():
        if line:
            part = line.decode('utf-8')
            if '"response":"' in part:
                text = part.split('"response":"')[1].split('"')[0]
                reply += text

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
