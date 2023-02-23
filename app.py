import firebase_admin
from firebase_admin import credentials, firestore, storage
from flask import Flask, request

app = Flask(__name__)

# Initialize Firebase Admin SDK with credentials
cred = credentials.Certificate('plant-disease-e5cf5-firebase-adminsdk-r5v8u-58303a0a53.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'plant-disease-e5cf5.appspot.com'
})

# Get a reference to the Firestore collection where you want to store the image URLs
db = firestore.client()
collection_ref = db.collection('images')

# Get a reference to the Cloud Storage bucket where you want to store the images
bucket = storage.bucket()

@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Get uploaded image from request
    image_file = request.files['image']

    # Save image file to Cloud Storage
    blob = bucket.blob(image_file.filename)
    blob.upload_from_file(image_file)

    # Get public URL for the image file
    url = blob.public_url

    # Save image URL to Firestore
    image_ref = collection_ref.document('new_image')
    image_ref.set({'url': url})

    # Return success response
    return {'message': 'Image uploaded to Cloud Storage and URL saved to Firestore successfully.'}

def predict_image(image_url):
    # Make a request to the Firebase ML API
    url = 'https://ml.googleapis.com/v1/projects/plant-disease/models/plant-disease-detector:predict'
    headers = {'Authorization': 'Bearer AIzaSyBHyVPAEkvH7Zv8UDqa2L_agqp-26epfQg'}
    data = {
        'instances': [
            {'image_uri': image_url}
        ]
    }
    response = requests.post(url, headers=headers, json=data)

    # Parse the prediction result from the response
    prediction = response.json()['predictions'][0]
    label = prediction['displayName']
    score = prediction['classification']['score']

    return label, score

# Example Flask route that retrieves an image URL from Firestore and makes a prediction with the model
@app.route('/predict_image', methods=['POST'])
def predict_image_route():
    # Get the image URL from Firestore
    image_ref = collection_ref.document('new_image')
    image_data = image_ref.get().to_dict()
    image_url = image_data['url']

    # Make a prediction with the model
    label, score = predict_image(image_url)

    # Return the prediction result
    return {'label': label, 'score': score}

if __name__ == '__main__':
    app.run(debug=True)
