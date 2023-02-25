from flask import Flask, request, jsonify
import requests
import urllib.request as urllib2

API_URL = "https://api-inference.huggingface.co/models/nickmuchi/yolos-small-plant-disease-detection"
headers = {"Authorization": "Bearer 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"}
app = Flask(__name__)

def query(data):
    # with open(filename, "rb") as f:
    #     data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

@app.route("/")
def index():
    return "Hello World!"

@app.route("/predict", methods=["GET"])
def predict():
    urlimg2 = "https://firebasestorage.googleapis.com/v0/b/farmlabslogin.appspot.com/o/users%2FGzojrnYywSaIvLB8Q85Aijbc7O73%2Fuploads%2F"
    if request.method == "GET":
        img = request.args['img']
        datas = img.split('/')
        urlimg2 = urlimg2 + datas[-1]
        urlimg2 = urlimg2 + '&token=' + request.args['token']
    #contents = urllib2.urlopen(urlimg2).read()
    contents = requests.get(urlimg).content
    return jsonify(query(contents))

if __name__ == "__main__":
    app.run(debug=True)

