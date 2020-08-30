from flask import Flask, jsonify, request, Response, Blueprint
from settings import *
from models.WordModel import *
import json

words_api = Blueprint('words_api', __name__)

invalidWordObjectErrorMsg = {
    "error": "Invalid word object passed in request",
    "helpString": "A word has the attributes: id, word and definitions."
}

doesExistWordObjectErrorMsg = {
    "error": "Word already exists"
}

doesNotExistWordObjectErrorMsg = {
    "error": "Word does not exist"
}

def validateWord(wordObject, put):
    return (
        "id" in wordObject or put
        and "word" in wordObject
    )

@app.route("/words")
def get_words():
    return jsonify({"words": Word.get_all_words()})

@app.route("/words", methods=["POST"])
def add_word():
    request_data = request.get_data()
    wordObject = json.loads(request_data)
    if (Word.doesExist(wordObject["id"])):
        response = Response(json.dumps(doesExistWordObjectErrorMsg), status=400, mimetype='application/json')
        return response
    if (validateWord(wordObject, False)):
        Word.add_word(wordObject["id"], wordObject["word"])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/words/" + str(wordObject['id'])
        return response
    else:
        response = Response(json.dumps(invalidWordObjectErrorMsg), status=400, mimetype='application/json')
        return response

@app.route("/words/<int:id>")
def get_word_by_id(id):
    return_value = Word.get_word(id)
    return jsonify(return_value)

@app.route('/words/<int:id>', methods=['PUT', 'PATCH'])
def replace_word(id):
    request_data = request.get_data()
    wordObject = json.loads(request_data)
    if (not Word.doesExist(id)):
        response = Response(json.dumps(doesNotExistWordObjectErrorMsg), status=400, mimetype='application/json')
        return response
    if (not validateWord(wordObject, True)):
        response = Response(json.dumps(invalidWordObjectErrorMsg), status=400, mimetype='application/json')
        return response
    Word.replace_word(id, wordObject["word"])
    response = Response("", status=204)
    return response

@app.route('/words/<int:id>', methods=['DELETE'])
def delete_word(id):
    if (Word.delete_word(id)):
        response = Response("", status=204)
        return response
    wordObjectNotFoundErrorMsg = {
        error: "Word with the id provided that was provided doesn't exist"
    }
    response = Response(json.dumps(wordObjectNotFoundErrorMsg), status="404", mimetype='application/json')
    return response