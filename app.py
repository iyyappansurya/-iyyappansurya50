from flask import Flask, request, jsonify
import requests

API_URL = "https://api-inference.huggingface.co/models/nickmuchi/yolos-small-plant-disease-detection"
headers = {"Authorization": "Bearer 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"}
app = Flask(__name__)

def query(data):
    # with open(filename, "rb") as f:
    #     data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            data = file.read()
            print(data)
            return jsonify(query(data))

if __name__ == "__main__":
    app.run(debug=True)

# files = {'file': open('test.jpg', 'rb')}
# r = requests.post(url, files=files)
