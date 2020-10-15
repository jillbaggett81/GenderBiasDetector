from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "Welcome to the Rec Letter Checker. WiP come back soon."

@app.route('/<name>')
def hello_name(name):
    return "Hey {}!".format(name)

if __name__ == '__main__':
    app.run(debug=True)
