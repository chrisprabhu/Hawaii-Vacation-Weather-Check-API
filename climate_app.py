from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/precipitation")
def precipitation():
    return 


if __name__ == "__main__":
    app.fun(debug=True)