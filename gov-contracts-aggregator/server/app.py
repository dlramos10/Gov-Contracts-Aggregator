from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "🚀 Titan Government Services API is Live!"

@app.route("/api/hello")
def hello():
    return {"message": "Hello from the server!"}

if __name__ == "__main__":
    app.run(debug=True)
