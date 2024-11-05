# The first thing we'll do is load all the libraries we'll be using
import os
from PIL import Image
import pytesseract
import requests
from bs4 import BeautifulSoup
from openai import AzureOpenAI
from openai import OpenAI
import streamlit as st

# Set the keys to access Azure OpenAI models
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("keyt")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("endpoint")


# 1. OBTAINING TIPS AND PROFILE MODELS

# Create a function to obtain information from the LinkedIn page with tips on building a good profile
def get_tips_from_url(url):
    """
    Retrieves tips from a webpage using web scraping.
    """
    # Make the request to get data from the webpage
    response = requests.get(url, verify=False)
    
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract the text from the page
    tips = soup.get_text()
    
    return tips

tips = get_tips_from_url("https://www.linkedin.com/business/sales/blog/profile-best-practices/17-steps-to-a-better-linkedin-profile-in-2017")

# Create a function to extract text from images we have of LinkedIn profiles
def get_profile_information(photos_folder):
    """
    Retrieves LinkedIn profile information from images using OCR.
    """
    # Set the path for the Tesseract OCR program used for text extraction
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\blanc\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

    # Create a list to store the text extracted from profile images
    profiles = []

    # Get the list of files in the photos folder
    photo_files = os.listdir(photos_folder)

    # Iterate over each file in the photos folder
    for file in photo_files:
        # Combine the path to the photos folder with the filename
        image_path = os.path.join(photos_folder, file)
        
        # Verify that the file is an image
        if image_path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # Open the image
            image = Image.open(image_path)
            
            # Perform OCR on the image
            text = pytesseract.image_to_string(image)
            
            # Add the text extracted to the profiles list
            profiles.append(text)

    # Join all profile examples into a single string
    profile_examples = '\n'.join(profiles)
    
    return profile_examples

profile_examples = get_profile_information(r'C:\Users\blanc\Documents\profiles')


# 2. CREATING THE NETWORK ASSISTANT CHATBOT
def network_assistant(user_question, tips, profile_examples, previous_messages):
    # Build the prompt with the user's question, context, and history
    prompt = f"""
    You are a professional LinkedIn assistant.
    Your task is to provide the user the best possible description for a LinkedIn profile.
    To provide the description, you will use the 'tips' given and the information from 'previous messages'.
    The profile description you provide should be inspired by the 'example of profiles'.
    Always respond in the same language used in the 'User Question'. 

    This is the 'User Question': {user_question}
    These are the 'tips': {tips}
    These are the 'example of profiles': {profile_examples}
    These are the 'previous messages': {previous_messages}

    Provide a response:
    """
    
    # Get the response from the OpenAI model
    client = AzureOpenAI(api_version="2023-05-15", azure_endpoint=os.getenv("endpoint"))
    completion = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    response = completion.choices[0].message.content

    return {"response": response}


# 3. USING STREAMLIT TO CONFIGURE THE APPLICATION

# Define the page title and icon
st.set_page_config(
        page_title="Network Assistant",
        page_icon="💬",
    )

# Set the page title
st.title("Network Assistant")

# Check if the message list is present in Streamlit's session state
if "messages" not in st.session_state:
    # If not present, initialize an empty list to store messages
    st.session_state.messages = []
    welcome_message = "Hello! I'm your Network Assistant. How can I help you today?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# Iterate over each message in the message list in Streamlit's session state
for message in st.session_state.messages:
    # Use st.chat_message context to display the message content in the chat
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Display an input box in the chat for the user to enter their question
if prompt := st.chat_input("How can I help you?"):
    # Add the user's message to the message list in Streamlit's session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display the user's question in the chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get the chatbot's response using the network_assistant function
    with st.spinner('Please wait while I am creating the best profile description for you'):
        response = network_assistant(user_question=prompt, tips=tips, profile_examples=profile_examples, previous_messages=st.session_state.messages)
        assistant_message = response["response"]

    # Add the chatbot's response to the message list in Streamlit's session state
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    
    # Display the chatbot's response in the chat
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
