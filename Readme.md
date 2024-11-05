**Network Assistant**

**Overview**

Network Assistant is a Python-based application that helps users optimize their LinkedIn profiles using Generative AI. By extracting relevant tips, analyzing sample profiles, and generating custom recommendations, this tool enables users to present themselves more effectively in the professional world.


**Project Structure and Code Explanation**

**1. Libraries and API Setup**

The project uses the following libraries:

PIL and pytesseract for Optical Character Recognition (OCR) to extract text from profile images.
requests and BeautifulSoup for web scraping to gather LinkedIn profile tips.
Azure OpenAI to access the GPT-4 language model for generating personalized descriptions.
Streamlit to build an interactive web interface.

**2. Data Gathering****

Web Scraping: 
The obtener_consejos_desde_url function scrapes tips for LinkedIn profiles from LinkedIn's blog using BeautifulSoup.
OCR for Profile Examples: 
The obtener_informacion_perfiles function uses Tesseract OCR to extract text from image files containing LinkedIn profiles.

**3. Generative AI Profile Assistant**

The network_assistant function serves as the core of the application. It constructs a prompt using the user's question, LinkedIn tips, and extracted profile examples. The prompt is sent to GPT-4 via Azure’s API, and a response is generated based on best practices for LinkedIn profile descriptions.

**4. User Interface with Streamlit**

Streamlit enables a chat-like interface where users can ask for LinkedIn profile advice and receive real-time responses. User inputs are handled, responses are displayed, and the conversation history is preserved to maintain context.

**How to Run**

Install required packages: pip install -r requirements.txt
Add your Azure OpenAI API keys to your environment.
Run the app with Streamlit: streamlit run app.py

**Summary**

Network Assistant combines web scraping, OCR, and generative AI to generate personalized LinkedIn profile advice. It’s an intuitive, interactive tool that simplifies the process of crafting impactful profiles for professional networking.
