from flask import Flask, jsonify,  request, render_template
import numpy as np
import process

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/recommend", methods=['POST', 'GET'])
def recommend():
    id = request.args['id']
    print(id)
    return jsonify(process.recommend(id))

if __name__ == '__main__':
    app.run()
