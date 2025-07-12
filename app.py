import streamlit as st
import pandas as pd
from util import load_data, preprocess_data, get_medicine_info, set_background
from model import train_model, find_medicine
import keyboard
from PIL import Image
import base64


#setting up the logo
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string
# Set background image
set_background('dr_penguin4.gif')
# Get base64 string for logo
logo_base64 = get_base64_image('45.png')
# Load and preprocess data
data_file = 'medicine_dataset.csv'
data = load_data(data_file)
data = preprocess_data(data)

# Train model
vectorizer, model = train_model(data)




# Custom CSS for background and styling
st.markdown(
    """
    <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main {
        background: linear-gradient(135deg, #f2f2f2, #e6e6e6);
        background-size: cover;
        min-height: 100vh;
    }
    h1 {
        color: black;
        text-align: center;
        margin-top: 20px;
        text-shadow: none;
    }
    .stTextInput label {
        color: black;
        font-weight: bold;
    }
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 6px;
        border: 2px solid #cccccc;
        color: black;
        padding: 10px;
    }
    .stTextInput input::placeholder {
        color: #777777;
    }
    .stTextInput input:focus {
        border-color: #0066cc;
        box-shadow: 0 0 8px rgba(0, 102, 204, 0.5);
    }
    .stButton button {
        background: linear-gradient(135deg, #0066cc, #3399ff);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 102, 204, 0.4);
    }
    .info-box {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #cccccc;
        padding: 20px;
        margin: 15px 0;
        border-radius: 8px;
        color: black;
        font-size: 16px;
        line-height: 1.5;
    }
    .warning {
        color: black;
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        padding: 12px;
        border: 2px solid #ff6666;
        border-radius: 8px;
        margin-top: 20px;
        background: #ffe6e6;
    }
    footer {
        background: transparent;
        color: #333333;
        padding: 20px 0;
        text-align: center;
    }
    .social-icons a {
        color: #333333;
        margin: 0 10px;
        font-size: 1.5em;
        transition: color 0.3s, transform 0.3s;
    }
    .social-icons a:hover {
        color: #0066cc;
        transform: scale(1.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.title("DR+ Medicine Information Finder")

# Initialize the session state
if 'search_button' not in st.session_state:
    st.session_state['search_button'] = False
if 'search_button' or ('medicine_name' and not st.session_state.get('searched', False)):
    st.session_state['searched'] = True
# Input field
medicine_name = st.text_input("Enter the name of the medicine:",placeholder='Enter the proper medicine name')

# JavaScript to trigger the search button on Enter key press
st.markdown(
    """
    <script type="text/javascript">
    document.addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
            document.querySelector('button[title="Search"]').click();
        }
    });
    </script>
    """,
    unsafe_allow_html=True
)

if st.button("Search", key="search_button_id"):
    st.session_state['search_button'] = True

if st.session_state['search_button']:
    if medicine_name:
        # Using the model to find the closest match
        index = find_medicine(vectorizer, model, medicine_name)
        medicine_info = get_medicine_info(data, data.iloc[index]['name'])

        # Filter out empty and 0 values
        uses = [use for use in medicine_info['uses'] if use]
        side_effects = [se for se in medicine_info['side_effects'] if se]
        substitutes = [sub for sub in medicine_info['substitutes'] if sub]

        # Display data in separate boxes
        st.write(f"### Uses of {medicine_name.capitalize()}")
        if uses:
            st.markdown('<div class="info-box">' + ''.join(uses) + '</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">No uses found</div>', unsafe_allow_html=True)

        st.write(f"### Side Effects of {medicine_name.capitalize()}")
        if side_effects:
            st.markdown('<div class="info-box">' + ''.join(side_effects) + '</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">No side effects found</div>', unsafe_allow_html=True)

        st.write(f"### Substitutes for {medicine_name.capitalize()}")
        if substitutes:
            st.markdown('<div class="info-box">' + ''.join(substitutes) + '</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">No substitutes found</div>', unsafe_allow_html=True)

        # Reset the search button state
        st.session_state['search_button'] = False
    else:
        st.write("Please enter a medicine name.")
st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css"
        integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />
    """,
    unsafe_allow_html=True
)
#IMPORTANT NOTICE 
st.markdown('<div class="warning">IT WILL ANALYZING WITH AI.IN ANY EMERGENCY CONDITION CONSULT WITH A DOCTOR.BEFORE TAKING SUBSTITUTE MEDICINE CONSULT WITH A DOCTOR.</div>', unsafe_allow_html=True)
        # Footer
st.markdown(
    """
    <footer>
        <div class="contain">
            <p class="animated-text">&copy; 2024 <a href="https://soumya-xd.github.io/" target="_blank">Soumya</a> Team. All rights reserved.</p>
            <div class="social-icons">
                <a href="https://www.facebook.com/soumya.singharoy.98" target="_blank"><i class="fab fa-facebook-f"></i></a>
                <a href="https://x.com/Soumya413876651" target="_blank" target="_blank"><i class="fab fa-twitter"></i></a>
                <a href="https://www.instagram.com/soumya_xd7/" target="_blank" target="_blank"><i class="fab fa-instagram"></i></a>
                <a href="https://www.linkedin.com/in/soumya-xd/" target="_blank"><i class="fab fa-linkedin"></i></a>
            </div>
        </div>
    </footer>
    """,
    unsafe_allow_html=True
)
