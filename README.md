# Car Damage Assessment Using VGG16

## About the project
The goal of the project is to classify severity of damage to cars inolved in traffic accidents so that insurers, vehicle owners can get a preliminary assessment of the damage.

Using transfer learning, the pre-trained VGG16 model was trained with images downloaded from the internet and labelled according to 5 classes:

1. Total loss = passenger compartment is crushed
2. Severe damage = front & side, back & side, front & back badly damaged
3. Moderate damage = front or back or side badly damaged
4. Minor damage = bumper damage, dings, dents, scratches
5. No damage = no damage

## Data & Package
Due to the file size limitation of 100Mb, the model with weights saved cannot be uploaded to this repository. However, you can download the data and the package [here](https://drive.google.com/drive/folders/1GG8vHnaA6knQSEBRIEFMKlVsqQX7T0-r?usp=sharing).

Please note that in the "data" folder:
1. "Raw Data" was the initial download from the internet without any preprocessing
2. "raw_data_01" has been re-labelled for moderate damage, severe damage, total loss classes
3. "predict" and "predict_02" contain a totally separate set of images that can be used for prediction

## Demo
The package was dockerized and deployed to Google Cloud Run (no GPU). View demo [here](https://cardamageassessment-b8efg37ubrah7jixsp8cnu.streamlit.app/). Please see findings below on the effects of GPU on prediction accuracy.

## Findings
Prediction accuracy using images in "predict_02" differed significantly, depending on whether the model was using GPU or not. For example, prediction using M2 Max with 30 core GPU in virtual environment with tensorflow-metal resulted in 80+% accuracy whilst prediction using separate virtual environment without tensorflow-metal resulted in only 60+% prediction accuracy on the same machine. Since Cloud Run does not have GPUs, we were unable to reproduce the 80+% prediction accuracy above. Deployment using a virtual machine with GPU in Compute Engine is being tested and results will be updated in this document.

### Update on 3 Oct 2023:
A virtual machine was set up on Google Compute Engine with Nvidia L4 GPU. Instead of using Docker images, the car_damage package was uploaded to the virtual machine via Google Cloud Storage. The package could run and detect the Nvidia L4 GPU, but the prediction results were no different from prediction without GPU. As of this update, no solution has been found to replicate the results obtained on the M2 Max with 30 core GPU.
