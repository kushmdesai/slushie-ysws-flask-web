from flask import Flask, render_template, request
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

with open("./sys-config-etc/system_configuration.txt") as f:
    sys_config = f.read()

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client()
app = Flask(__name__)

@app.route("/")
def index():
    user_name = 'kcoder'
    return render_template('index.html')

@app.route('/chat')
def chat():
    user_input = request.form['user_input']

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[user_input],
        config=types.GenerateContentConfig(
            system_instruction=sys_config
        )
    )
@app.route('/about')
def about():
    user_name = "about"
    return render_template('about.html')

if __name__ == "__main__":
    app.run(port=5000, debug = True)