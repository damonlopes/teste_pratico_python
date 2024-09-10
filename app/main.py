from flask import Flask, request
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, world!'

@app.route('/get_flights')
def get_info_flights():
    teste = request.args.get("teste")
    if teste is not None:
        return teste
    else:
        return os.environ["CHAVE_API"]

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)