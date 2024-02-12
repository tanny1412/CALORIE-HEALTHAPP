### Health Mangament APP

from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Load Google Gemini Pro Vision

def get_gemini_response(input_text, image_data, prompt_text):
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-pro-vision')
    
    # Prepare the contents as a list containing the prompt and the image data
    contents = [prompt_text, image_data]  # Use 'contents' instead of 'content'
    
    # Call generate_content with the correct parameter name 'contents'
    response = model.generate_content(contents=contents)  # Use 'contents=' here
    
    return response.text
 

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Prepare the image data in the format expected by the API
        image_data = {
            'mime_type': uploaded_file.type,  # The MIME type of the image
            'data': uploaded_file.getvalue()  # The image data as bytes
        }
        return image_data
    else:
        raise FileNotFoundError("No file uploaded")
    

st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")


uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me the total calories")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----


"""


user_input = st.text_input("Input Prompt: ", key="input")  # Renamed variable for clarity

if submit and uploaded_file is not None:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(user_input, image_data, input_prompt)  # Adjusted variable names
    st.subheader("The Response is")
    st.write(response)
else:
    st.write("Please upload an image.")
    #