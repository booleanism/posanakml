from typing import Dict, Tuple
from flask import Flask, request, jsonify
import pickle
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)


with open('stunting_model.sav', 'rb') as f:
    model = pickle.load(f)

clf_class = ['tinggi', 'normal', 'stunting', 'xstunting']
n_class = 4

def detect(umur: int, jenis_kelamin: int, tinggi_badan: int) -> Tuple[str, int] | None:
    pred = model.predict([[umur, jenis_kelamin, tinggi_badan]])
    res = n_class - 1 - pred[0].item()
    if res < n_class:
        return clf_class[res], res
    
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
    print(resp_obj)
    return jsonify(resp_obj), 200

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
