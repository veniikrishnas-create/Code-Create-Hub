
from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API key using Render Environment Variables
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)


# Homepage route
@app.route("/", methods=["GET"])
def home():
    return "Code-Create-Hub Backend is Running!"


# Gemini AI chat route
@app.route("/ask", methods=["POST"])
def ask_gemini():
    try:
        if not api_key:
            return jsonify({
                "error": "Gemini API key is not configured."
            }), 500

        data = request.get_json(silent=True) or {}
        question = data.get("prompt", "").strip()

        if not question:
            return jsonify({
                "error": "Please provide a prompt."
            }), 400

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(question)

        return jsonify({
            "reply": response.text
        })

    except Exception:
        app.logger.exception("Error while generating Gemini response")
        return jsonify({
            "error": "Unable to generate a response. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=False)
