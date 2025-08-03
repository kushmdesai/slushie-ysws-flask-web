# SlushBot

## Description

If you are seeing this then you probably know about the [slushie ysws](https://slushies.hackclub.com/). Its where you make a flask application and you get $5-10 to buy a slushie. Have you ever bothered to stop and think from the slushie's point of view ? :)

Well you no longer have to, just head over to the [slushbot website](https://slushbot.kcoder.hackclub.app/) and chat you head of with a fun,and a little bit sarcastic some times, sentient slushy!

## Pictures

Home Page
![homepage](/pictures/homepage.png)

Chat Page
![chatpage](/pictures/chatpage.png)

About Page
![aboutpage](/pictures/aboutpage.png)


## Main Code File
```from flask import Flask, render_template, request, session
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os, uuid

with open("./sys-config-etc/system_configuration.txt") as f:
    sys_config = f.read()

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
print(API_KEY)
port = int(os.environ.get('FLASK_PORT', 3000))
print(port)
client = genai.Client()
app = Flask(__name__)
key =str(uuid.uuid4()) 
app.secret_key = key

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/chat', methods=["GET","POST"])
def chat():
    if 'history' not in session:
        session['history'] = []
    user_input = request.form.get('user_input')

    if not user_input or user_input.strip() == "":
        user_input = "Start the conversation/ Hi"
    else:
        session['history'].append({"role": "user", "text": user_input})
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[user_input],
        config=types.GenerateContentConfig(
            system_instruction=sys_config
        )
    )
    session['history'].append({"role":"gemini", "text":response.text})
    session.modified = True 
    return render_template('chat.html', history=session['history'])
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    pass # <-- maybe this will work? :( pretty desperate by now
```

## Usage of Ai 

I can promise you that I did not use any ai whatsoever while coding. I have written all the code by myself. I also got the setup.sh file from the nest tutorial.

The only time that I did use ai was when for some reason the nest was not working so I gave the error message (which I was unable to understand) to gemini which told me I had to wait a while before I could get an ssl certificate.

## Thanks So Much and bye!!