from flask import Flask, render_template, request, stream_with_context, Response
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
    return render_template('index.html')

@app.route('/chat', methods=["GET","POST"])
def chat():
    user_input = request.form.get('user_input')

    if not user_input or user_input.strip() == "":
        user_input = "Start the conversation/ say hi"

    def generate():
        response = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=[user_input],
            config=types.GenerateContentConfig(
                system_instruction=sys_config
            )
        )
        for chunk in response:
                yield chunk.text
    chatresponse = "".join(generate())
    return render_template('chat.html',chatresponse=chatresponse)
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(port=5000, debug = True)