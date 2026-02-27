import uuid
import errors.base as base
import modules
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


SetRouter = Blueprint('set', __name__)

@SetRouter.route('/', methods=['POST'])
@jwt_required()
def create_set():
    identity = get_jwt_identity()
    data = request.get_json(silent=True)
    if data is None: raise base.SetValidationError("data empty.")
    
    modules.set.create_set(
        set_id=uuid.uuid4().hex[:16],
        title=data.get('title', ""),
        description=data.get('description', ""),
        is_public=1 if data.get('is_public', 0) == 1 else 0,
        owner_id=identity,
    )
    return jsonify({"message": "set created"}), 201


@SetRouter.route('/analyze', methods=['POST'])
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
    

@SetRouter.route('/<username>', methods=['GET'])
@jwt_required(optional=True)
def get_sets(username):
    identity = get_jwt_identity()
    user_sets = modules.set.get_user_sets(username)

    result = []
    if username == identity: result = user_sets
    else: result = [s for s in user_sets if s['is_public'] == 1]
    return jsonify({"sets": result}), 200


@SetRouter.route('/<username>/<set_id>', methods=['GET'])
@jwt_required(optional=True)
def get_set_detail(username, set_id):
    identity = get_jwt_identity()
    user_set = modules.set.get_user_set(set_id, username)
    if user_set.get('is_public', 0) == 0 and username != identity: 
        raise base.ForbiddenError()
    set_words = modules.word.getWords(set_id)

    return jsonify({
        "set_info": user_set,
        "words": set_words
    })


@SetRouter.route('/<username>/<set_id>/words', methods=['POST'])
@jwt_required()
def setWords(username, set_id):
    identity = get_jwt_identity()
    if username != identity: 
        raise base.ForbiddenError()
    
    data = request.get_json(silent=True)
    if data is None: raise base.SetValidationError("data is required.")

    modules.word.setWords(set_id, data.get("words", []))
    return jsonify({"message": "words added"}), 201


@SetRouter.route('/<username>/<set_id>/words', methods=['PATCH'])
@jwt_required()
def editWords(username, set_id):
    identity = get_jwt_identity()
    if username != identity: 
        raise base.ForbiddenError()
    
    data = request.get_json(silent=True)
    if data is None: raise base.SetValidationError("data empty.")
    modules.word.updateWords(set_id, data.get("words", []))
    return jsonify({"message": "words updated"}), 200


@SetRouter.route('/<username>/<set_id>/words', methods=['DELETE'])
@jwt_required()
def deleteWords(username, set_id):
    identity = get_jwt_identity()
    if username != identity: 
        raise base.ForbiddenError()

    data = request.get_json(silent=True)
    if data is None: raise base.SetValidationError("data empty.")
    modules.word.deleteWords(set_id, data.get("word_ids", []))
    return jsonify({"message": "words updated"}), 200