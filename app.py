from flask import Flask
from flask.templating import render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/<name>')
def hello_name(name):
    return "Hey {}!".format(name)

if __name__ == '__main__':
    app.run(debug=True)
