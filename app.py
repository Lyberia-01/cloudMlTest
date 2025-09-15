import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/weather-feedback', methods=['POST'])
def get_weather_feedback():
    try:
        data = request.json  # Expecting JSON from ESP32
        if not data:
            return jsonify({"error": "No JSON data received."}), 400

        # Construct a more specific prompt for Gemini
        prompt = f"""
        Analyze the following real-time sensor data from an IoT device.
        Provide a concise, sharp, and app-inclined response for a home automation app.
        The data includes temperature, humidity, and a smoke sensor reading.
        Be helpful and actionable.

        Sensor Data: {data}
        """

        gemini_response = model.generate_content(prompt)
        feedback = gemini_response.text

        return jsonify({
            "status": "success",
            "received_data": data,
            "gemini_feedback": feedback
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)