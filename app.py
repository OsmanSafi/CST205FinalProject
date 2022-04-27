from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def landingPage():
    return render_template('landingPage.html')

app.run() 

