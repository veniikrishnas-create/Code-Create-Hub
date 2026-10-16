
from flask import Flask, request, jsonify, send_from_directory
import os
import google.generativeai as genai

app = Flask(__name__)

# Get Gemini API key from Render environment variables
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)


# Welcome page
@app.route("/", methods=["GET"])
def home():
    return send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        "welcome page.html"
    )


# Gemini AI endpoint
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
        app.logger.exception("Gemini API request failed")
        return jsonify({
            "error": "Unable to generate a response. Please try again."
        }), 500


# Run locally
if __name__ == "__main__":
    app.run(debug=False)
