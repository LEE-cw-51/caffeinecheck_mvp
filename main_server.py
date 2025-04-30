from flask import Flask, request, jsonify
from scripts.add_record import handle_add_record
from scripts.remove_record import handle_remove_record
from scripts.feedback import handle_feedback
from scripts.recommendation import get_recommendation

app = Flask(__name__)

@app.route("/add_record", methods=["POST"])
def add_record():
    result, status = handle_add_record(request.json)
    return jsonify(result), status

@app.route("/remove_record", methods=["DELETE"])
def remove_record():
    result, status = handle_remove_record(request.json)
    return jsonify(result), status

@app.route("/feedback", methods=["POST"])
def feedback():
    result, status = handle_feedback(request.json)
    return jsonify(result), status

@app.route("/get_recommendation", methods=["GET"])
def recommendation():
    result, status = get_recommendation()
    return jsonify(result), status

if __name__ == "__main__":
    app.run(debug=True)
