from flask import Flask,render_template

###################
# Initialization  #
###################
app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

@app.route('/')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True,port='8080')