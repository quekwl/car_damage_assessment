# Import packages and modules
import pandas as pd
import numpy as np
import cv2
# import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# Instantiate api
app = FastAPI()

# Load model in memory for faster prediction
model_path = "/car_damage/api/model_vgg16_01a.h5"
app.state.model = load_model(model_path)
custom_model_vgg16 = app.state.model


# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define root endpoint
@app.get("/")
def index():
    return {"fast_api_prod_root": True}


# Define prediction endpoint
@app.post("/predict")
async def predict(image: UploadFile):

    # Process uploaded image
    file_content = await image.read()
    image = cv2.imdecode(np.frombuffer(file_content, np.uint8), -1)
    image = cv2.resize(image, (224, 224))

    # Predict
    class_names = ['moderate_damage', 'no_damage', 'severe_damage', 'minor_damage', 'total_loss']
    image = np.expand_dims(image, axis=0)
    result = custom_model_vgg16.predict(image)

    return {"prediction": class_names[np.argmax(result)]}
