from flask import Flask, request, abort, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    json = request.get_json()
    numerator = json.get('numerator')
    denominator = json.get('denominator')
    if denominator == 0:
        abort(400)
    else:
        return jsonify(result=numerator / denominator)