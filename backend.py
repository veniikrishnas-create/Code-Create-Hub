from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# ✅ Add your Gemini API key here (safe, server-side)
genai.configure(api_key="AIzaSyDiKL2H5dhu1_ZCYeIudEqPdI0mwd6btXY")

@app.route("/ask", methods=["POST"])
def ask_gemini():
    data = request.get_json()
    question = data.get("prompt", "")

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(question)

    return jsonify({"reply": response.text})

if __name__ == "__main__":
    app.run(debug=True)
