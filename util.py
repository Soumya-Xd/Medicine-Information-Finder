import pandas as pd
import base64
import streamlit as st
import numpy as np
from PIL import Image, ImageOps

def set_background(image_file):
    """
    This function sets the background of a Streamlit app to an image specified by the given image file.

    Parameters:
        image_file (str): The path to the image file to be used as the background.

    Returns:
        None
    """
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
            background-size: 45%;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def preprocess_data(data):
    data['name'] = data['name'].str.lower()
    return data

def get_medicine_info(data, medicine_name):
    medicine_name = medicine_name.lower()
    result = data[data['name'] == medicine_name]
    if not result.empty:
        uses = "\n".join([result['use'].values[0]]) if pd.notna(result['use'].values[0]) else "No uses found"
        side_effects = "\n".join([result['sideEffect'].values[0]]) if pd.notna(result['sideEffect'].values[0]) else "No side effects found"
        substitutes = "\n".join([result['substitute'].values[0]]) if pd.notna(result['substitute'].values[0]) else "No substitutes found"
        return {'uses': uses, 'side_effects': side_effects, 'substitutes': substitutes}
    else:
        return {'uses': "Medicine not found", 'side_effects': "Medicine not found", 'substitutes': "Medicine not found"}
