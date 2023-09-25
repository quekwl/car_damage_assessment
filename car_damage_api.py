import requests
import io
import streamlit as st
from PIL import Image
import streamlit as st

api_endpoint = "https://car-damage-35ftdc3l5a-ew.a.run.app/predict"

st.set_page_config(
    page_title="Car Damage Assessment Analyzer 🚗💥",
    page_icon=":car:",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("Car Damage Analyzer 🚗💥")
image = st.file_uploader("OH NO! You just got into an accident 😱: Upload an image below to check severity of damage of your vehicle below 👇", type=["jpg", "png", "jpeg"])
st.markdown("The Car Damage Assessment Analyzer will categorize your car into 1 of 5 categories:")

custom_css ="""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #000000; /* Black background */
    color: #FFFFFF; /* White text color */
}
/* Specify text color for specific elements */
h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF; /* White text color for headings */
}
</style>
"""

image_paths = [
    "chermaine_predict/totalloss.jpg",
    "chermaine_predict/severedamage.JPG",
    "chermaine_predict/moderatedamage.JPG",
    "chermaine_predict/minordamage.jpg",
    "chermaine_predict/nodamage.jpg",
]

captions = [
    "Total Loss",
    "Severe Damage",
    "Moderate Damage",
    "Minor Damage",
    "No Damage"
]

descriptions = {
    "Total Loss":     "The car is completely crushed.",
    "Severe Damage":  "The car has significant damage.",
    "Moderate Damage":"The car has moderate damage.",
    "Minor Damage":   "The car has minor damage.",
    "No Damage":      "The car has no visible damage."
}

if len(captions) != len(image_paths):
    st.error("Number of captions must match the number of images.")
else:
    image_size = (400, 400)
    image_row = st.columns(len(image_paths))
    for i in range(len(image_paths)):
        image_path = image_paths[i]
        caption = captions[i]
        description = descriptions.get(caption, "Description not available.")

        img = Image.open(image_path)
        img = img.resize(image_size) #Resizing

        with image_row[i]:
            st.image(img, caption=caption, use_column_width=True)
            st.write(f"<p style='font-size: 11px;'>{description}</p>", unsafe_allow_html=True)

# Display the uploaded image
if image is not None:
    st.image(image, caption="Uploaded Image", width=500)

    # Button to trigger the prediction
    if st.button("Predict"):
        img = Image.open(image)
        img = img.resize((224, 224))
        img_bytes = io.BytesIO() # Convert image to bytes
        img.save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()

        # Make a POST request to the FastAPI API
        response = requests.post(api_endpoint, files={"image": img_bytes})

        if response.status_code == 200:
            prediction = response.json()["prediction"]

            prediction_labels = {
                "total_loss": "Total Loss",
                "severe_damage": "Severe Damage",
                "moderate_damage": "Moderate Damage",
                "minor_damage": "Minor Damage",
                "no_damage": "No Damage"
            }
            prediction_label = prediction_labels.get(prediction, "Unknown prediction")

            # st.success(f"Prediction: {prediction}")
            st.write(f'<div style="font-size: 40px;">Prediction: {prediction_label}</div>', unsafe_allow_html=True)

            if prediction == "no_damage":
                slider = st.slider('Price Range Indicator (in SG$)', value=0, min_value=0, max_value=50000)
                st.write(f'<div style="font-size: 25px;">Your car looks good 👍: No Repair Needed </div>', unsafe_allow_html=True)
            elif prediction == "minor_damage":
                slider = st.slider('Price Range Indicator (in SG$)', value=10000, min_value=0, max_value=50000)
                st.write(f'<div style="font-size: 25px;">Your car seems to have a minor scratch/dent 🫢: Estimate Repair cost = Less than 10k</div>', unsafe_allow_html=True)
            elif prediction == "moderate_damage":
                slider = st.slider('Price Range Indicator (in SG$)', value=20000, min_value=0, max_value=50000)
                st.write(f'<div style="font-size: 25px;">Your car seems to be moderately damaged 😔: Estimate Repair cost = From 10k to 20k</div>', unsafe_allow_html=True)
            elif prediction == "severe_damage":
                slider = st.slider('Price Range Indicator (in SG$)', value=30000, min_value=0, max_value=50000)
                st.write(f'<div style="font-size: 25px;">Your car seems to be severly damaged 😣: Estimate Repair cost = From 20k to 30k</div>', unsafe_allow_html=True)
            elif prediction == "total_loss":
                slider = st.slider('Price Range Indicator (in SG$)', value=50000, min_value=0, max_value=50000)
                st.write(f'<div style="font-size: 25px;">Your car seems to be a total loss 😖: Estimate Repair cost = More than 30k</div>', unsafe_allow_html=True)
                st.write(f'<div style="font-size: 23px;">The cost to repair your car might be more expensive than getting a new vehicle!</div>', unsafe_allow_html=True)

        else:
            st.error("Failed to get prediction from the API 🚨.")
