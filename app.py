from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    user_name = 'kcoder'
    return render_template('index.html', user_name=user_name)

@app.route('/testing')
def testing():
    user_name = "TESTING"
    return render_template('testing.html', user_name=user_name)

if __name__ == "__main__":
    app.run(port=5000, debug = True)

