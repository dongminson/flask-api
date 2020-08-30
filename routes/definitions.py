from flask import Flask, jsonify, request, Response, Blueprint
from settings import *
from models.DefinitionModel import *
import json

definitions_api = Blueprint('definitions_api', __name__)

invalidDefinitionObjectErrorMsg = {
    "error": "Invalid definition object passed in request",
    "helpString": "A definition has the attributes: id, partOfSpeech, definition and wordId."
}

doesExistDefinitionObjectErrorMsg = {
    "error": "Definition already exists",
}

doesNotExistDefinitionObjectErrorMsg = {
    "error": "Definition does not exist",
}

def validateDefinition(definitionObject, put):
    return (
        "id" in definitionObject or put
        and "partOfSpeech" in definitionObject
        and "definition" in definitionObject
        and "wordId" in definitionObject
    )

@app.route("/definitions")
def get_definitions():
    return jsonify({"definitions": Definition.get_all_definitions()})

@app.route("/definitions", methods=["POST"])
def add_definition():
    request_data = request.get_data()
    definitionObject = json.loads(request_data)
    if(Definition.doesExist(definitionObject["id"])):
        response = Response(json.dumps(doesExistDefinitionObjectErrorMsg), status=400, mimetype='application/json')
        return response
    if (validateDefinition(definitionObject, False)):
        Definition.add_definition(definitionObject["id"], definitionObject["partOfSpeech"], definitionObject["definition"], definitionObject["wordId"])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/definitions/" + str(definitionObject['id'])
        return response
    else:
        response = Response(json.dumps(invalidDefinitionObjectErrorMsg), status=400, mimetype='application/json')
        return response

@app.route("/definitions/<int:id>")
def get_definition_by_id(id):
    return_value = Definition.get_definition(id)
    return jsonify(return_value)

@app.route('/definitions/<int:id>', methods=['PUT'])
def replace_definition(id):
    request_data = request.get_data()
    definitionObject = json.loads(request_data)
    if (not Definition.doesExist(id)):
        response = Response(json.dumps(doesNotExistDefinitionObjectErrorMsg), status=400, mimetype='application/json')
        return response
    if (not validateDefinition(definitionObject, True)):
        response = Response(json.dumps(invalidDefinitionObjectErrorMsg), status=400, mimetype='application/json')
        return response
    Definition.replace_definition(id, definitionObject["partOfSpeech"], definitionObject["definition"], definitionObject["wordId"])
    response = Response("", status=204)
    return response

@app.route('/definitions/<int:id>', methods=['PATCH'])
def update_definition(id):
    request_data = request.get_data()
    definitionObject = json.loads(request_data)
    if (not Definition.doesExist(id)):
        response = Response(json.dumps(doesNotExistDefinitionObjectErrorMsg), status=400, mimetype='application/json')
        return response
    if ("partOfSpeech" in definitionObject):
        Definition.update_definition_part_of_speech(id, definitionObject["partOfSpeech"])
    if ("definition" in definitionObject):
        Definition.update_definition_definition(id, definitionObject["definition"])
    if ("wordId" in definitionObject):
        Definition.update_definition_word_id(id, definitionObject["wordId"])
    
    response = Response("", status=204)
    response.headers['Location'] = "/definitions/" + str(id)
    return response
           
@app.route('/definitions/<int:id>', methods=['DELETE'])
def delete_definition(id):
    if (Definition.delete_definition(id)):
        response = Response("", status=204)
        return response
    definitionObjectNotFoundErrorMsg = {
        error: "Definition with the id provided that was provided doesn't exist"
    }
    response = Response(json.dumps(definitionObjectNotFoundErrorMsg), status="404", mimetype='application/json')
    return response
