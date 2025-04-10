from flask import Flask, render_template, request, jsonify
import requests

# Create the Flask app instance
app = Flask(__name__)


# Route for the homepage
@app.route("/")
def index():
    return render_template("index.html")


# Route to handle POST requests for emotion detection
@app.route("/analyze", methods=["POST"])
def analyze():
    # Get JSON data from the frontend request
    data = request.get_json()
    try:
        # Forward the data to the machine learning client
        response = requests.post("http://ml-client:5001/analyze", json=data)
        return jsonify(response.json())
    except Exception as error:
        # If anything goes wrong, return an error message with status code 500
        return jsonify({"error": str(error)}), 500


# Start the Flask app on host 0.0.0.0 and port 8888
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
