import errors.base as base
import modules
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


WordRouter = Blueprint('words', __name__)

@WordRouter.route('/analyze', methods=['POST'])
@jwt_required()
def analyzeWords():
    data = request.get_json(silent=True)
    if data is None: raise base.SetValidationError("data empty.")

    words = data.get("words", [])
    responses = modules.word.getWordsDetail(words)
    if responses == []: raise base.WordError("words is empty") 

    result = []
    for response in responses:
        id = response['_id']
        word = response['word']
        definitions_result = []
        definitions = response['definitions']
        for definition in definitions:
            definitions_result.append({ 
                "ko": definition['ko'], 
                "pos": definition["pos"] 
            })
        result.append({
            "id": id,
            "word": word,
            "definitions": definitions_result
        })
    
    return jsonify({"data": result}), 200
    

@WordRouter.route('/<username>/<set_id>', methods=['POST'])
@jwt_required()
def addWords(username, set_id):
    identity = get_jwt_identity()
    if username != identity: raise base.ForbiddenError()
    modules.set.is_valid_set(set_id, identity)
    
    data = request.get_json(silent=True)
    if data is None: raise base.SetValidationError("data empty.")

    modules.word.setWords(set_id, data.get("words", []))
    return jsonify({"message": "words updated"}), 200
    

@WordRouter.route('/<username>/<set_id>', methods=['PATCH'])
@jwt_required()
def editWords(username, set_id):
    identity = get_jwt_identity()
    if username != identity: raise base.ForbiddenError()
    modules.set.is_valid_set(set_id, identity)
    
    data = request.get_json(silent=True)
    if data is None: raise base.SetValidationError("data empty.")

    modules.word.updateWords(set_id, data.get("words", []))
    return jsonify({"message": "words updated"}), 200


@WordRouter.route('/<username>/<set_id>', methods=['DELETE'])
@jwt_required()
def deleteWords(username, set_id):
    identity = get_jwt_identity()
    if username != identity: raise base.ForbiddenError()
    modules.set.is_valid_set(set_id, identity)

    data = request.get_json(silent=True)
    if data is None: raise base.SetValidationError("data empty.")

    modules.word.deleteWords(set_id, data.get("word_ids", []))
    return jsonify({"message": "words updated"}), 200
