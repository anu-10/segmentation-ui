from flask import Flask, jsonify, request, send_file
from flask_restful import Resource, Api 
from flask_cors import CORS
from model import segmentation_model
import cv2
import os
import numpy as np
from PIL import Image as pilimage
# creating the flask app 
app = Flask(__name__) 

# creating an API object   
api = Api(app) 
allowed_origins = [
    "http://localhost:3000"
]
 
cors = CORS(app, origins=allowed_origins)

class Home(Resource):
    def get(self):
        return jsonify('Hello')

class Image(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
        segment = segmentation_model()
        images = segment.segmentation()
        save_path = '../segmented/saved_image0.png'
        I = images[len(images)//2, :, :, 0]
        I8 = (((I - I.min()) / (I.max() - I.min())) * 255).astype(np.uint8)
        image = pilimage.fromarray(I8)
        image.save(save_path)
        return send_file(save_path)
  
  
    # Corresponds to POST request 
    def post(self): 
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file:
            file.save('../images/file.nii.gz')
            return jsonify({'message': 'File uploaded successfully'})

        
  

  
  
  
# adding the defined resources along with their corresponding urls 
api.add_resource(Home, '/')
api.add_resource(Image, '/image') 

  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 