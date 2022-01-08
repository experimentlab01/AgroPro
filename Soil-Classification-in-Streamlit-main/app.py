import streamlit as st
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image, ImageOps
import numpy as np
import base64

st.title(' ')
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
       data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
        <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
        ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('background.png')


def teachable_machine_classification(img, file):
    np.set_printoptions(suppress=True)

    # Load the model
    model = keras.models.load_model(file)

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = img
    # image = Image.open(img_name).convert('RGB')
    # image = cv2.imread(image)

    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    #image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    prediction = model.predict(data)
    return prediction

new_title = '<p style="font-family:Fjord One; color:#040720; font-size: 42px;"><b>Soil Classification</b></p>'
st.markdown(new_title, unsafe_allow_html=True)
new_title = '<p style="font-family:Fjord One; color:Black; font-size: 43px;"><b>Upload an Image</b></p>'
st.markdown(new_title, unsafe_allow_html=True)
new_title = '<p style="font-family:Fjord One; color:Black; font-size: 23px;"><b>Choose a Image</b></p>'
st.markdown(new_title, unsafe_allow_html=True)

uploaded_file = st.file_uploader(" ", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded IMage.', use_column_width=True)
    st.write("Classifying Image")
    label = teachable_machine_classification(image, 'keras_model.h5')
    blacksoil= (label[0][0])
    cindersoil= (label[0][1])
    lateritesoil= (label[0][2])
    peatsoil= (label[0][3])
    yellowsoil= (label[0][4])
    if blacksoil >= 0.6:
        st.title("It is blacksoil")
    elif cindersoil >= 0.6:
        st.title("It is cinder soil")
    elif lateritesoil >= 0.6:
        st.title(" It is laterite soil")
    elif peatsoil >= 0.6:
        st.title("It is peat soil")
    elif yellowsoil >= 0.6:
        st.title("It is yellow soil")
