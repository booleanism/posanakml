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

def wrap_jk(content: str | int) -> int:
    if type(content) != str:
        try:
            return int(content)
        except:
            raise Exception('invalid value')

    if content == 'laki-laki':
        return 1
    return 0

def val_umur(content: str) -> int:
    try:
        umur = int(content)
        if umur <= 60 and umur >= 0:
            return umur
        raise Exception('invalid months')
    except:
        raise Exception('invalid value')

def wrap_tb(content: str | int) -> int:
    if type(content) == str:
        try:
            return int(content)
        except:
            raise Exception('invalid value')
    return int(content)


@app.route('/', methods=['POST'])
def predict():
    resp_obj: Dict[str, str | int] = {}

    if request.headers.get('Content-Type') != 'application/json':
        resp_obj['result'] = -1
        resp_obj['message'] = 'mismatch content-type'
        return jsonify(resp_obj), 400

    try:
        content = request.get_json()

        if content is None:
            resp_obj['result'] = -1
            resp_obj['message'] = 'missing request body'
            return jsonify(resp_obj), 400
    except:
        resp_obj['result'] = -1
        resp_obj['message'] = 'missing request body'
        return jsonify(resp_obj), 400

    try:
        umur = val_umur(content['umur'])
        jk = wrap_jk(content['jenis_kelamin'])
        tb = wrap_tb(content['tinggi_badan'])
    except Exception as ex:
        resp_obj['result'] = -1
        resp_obj['message'] = ex.args[0]
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
