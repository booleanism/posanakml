from typing import Dict, Tuple
from flask import Flask, request, jsonify
import pickle
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)


with open('stunting_model.sav', 'rb') as f:
    model = pickle.load(f)

def detect(umur: int, jenis_kelamin: int, tinggi_badan: int) -> Tuple[str, int] | None:
    pred = model.predict([[umur, jenis_kelamin, tinggi_badan]])
    if pred[0] == 3:
        return 'tinggi', 0
    if pred[0] == 2:
        return 'normal', 1
    if pred[0] == 1:
        return 'stunting', 2
    if pred[0] == 0:
        return 'xstunting', 3
    
    return None

@app.route('/', methods=['POST'])
def predict():
    resp_obj: Dict[str, str | int] = {}
    try:
        content = request.json

        if content is None:
            raise Exception("request body are None")
    except:
        resp_obj['result'] = -1
        resp_obj['message'] = 'missing request body'
        return jsonify(resp_obj), 400

    try:
        umur = int(content['umur'])
        jk = int(content['jenis_kelamin'])
        tb = int(content['tinggi_badan'])
    except:
        resp_obj['result'] = -1
        resp_obj['message'] = 'missing json field'
        return jsonify(resp_obj), 400

    pred = detect(umur, jk, tb)
    if pred is None:
        resp_obj['result'] = -1
        resp_obj['message'] = 'could not predict'
        return jsonify(resp_obj), 500

    resp_obj['result'] = pred[1]
    resp_obj['message'] = pred[0]
    return jsonify(resp_obj), 200

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
