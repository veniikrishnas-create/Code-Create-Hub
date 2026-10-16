from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# ✅ Add your Gemini API key here (safe, server-side)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/ask", methods=["POST"])
def ask_gemini():
    data = request.get_json(silent=True) or {}
    question = data.get("prompt", "")

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(question)

    return jsonify({"reply": response.text})

if __name__ == "__main__":
    app.run(debug=True)
