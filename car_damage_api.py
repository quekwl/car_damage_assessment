import requests
import io
import streamlit as st
from PIL import Image
import streamlit as st

# Define custom CSS to set the background image
# custom_css ="""
# <style>
# [data-testid="stAppViewContainer"] {
#     background-image: url("");
#     background-size: cover;
# }
# /* Add the custom CSS to expand the width */
# body {
#     width: 500%;  /* Adjust the width as needed */
#     margin: 50 auto; /* Center the content */
# }
# </style>
# """

api_endpoint = "https://car-damage-35ftdc3l5a-ew.a.run.app/predict"

st.set_page_config(
    page_title="Car Damage Assessment Analyzer 🚗💥",
    page_icon=":car:",
    layout="wide",  # Use a wide layout
    initial_sidebar_state="expanded",  # Expand the sidebar by default
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
    "chermaine_predict/minordamage.jpg",
    "chermaine_predict/severedamage.JPG",
    "chermaine_predict/moderatedamage.JPG",
    "chermaine_predict/totalloss.jpg",
    "chermaine_predict/nodamage.jpg",
]
captions = [
    "Total Loss",
    "Severe Damage",
    "Moderate Damage",
    "Minor Damage",
    "No Damage"
]


if len(captions) != len(image_paths):
    st.error("Number of captions must match the number of images.")
else:
    # Define the size for all images
    image_size = (400, 400)
    # Create a grid for displaying images side by side with captions
    image_row = st.columns(len(image_paths))
    for i in range(len(image_paths)):
        image_path = image_paths[i]
        caption = captions[i]
        # Load and resize the image
        img = Image.open(image_path)
        img = img.resize(image_size)
        # Display the resized image with the specified caption
        with image_row[i]:
            st.image(img, caption=caption, use_column_width=True)


# Display the uploaded image
if image is not None:
    st.image(image, caption="Uploaded Image.", width=400)

    # Button to trigger the prediction
    if st.button("Predict"):
        # Prepare the image for prediction
        img = Image.open(image)
        img = img.resize((224, 224))  # Adjust the size based on your model's requirements

        # Convert image to bytes
        img_bytes = io.BytesIO()
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
        else:
            st.error("Failed to get prediction from the API.")
