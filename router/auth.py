import errors.base as base
import modules
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, set_refresh_cookies, unset_jwt_cookies


AuthRouter = Blueprint('auth', __name__)


@AuthRouter.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if data is None: raise base.AuthError("empty data.")

    # id, pw 가져오기
    input_id = data.get('id')
    input_password = data.get('password')
    if not all([input_id, input_password]):
        raise base.AuthError("ID or password cannot be empty.")

    # 로그인 시도. 실패 시 raise
    modules.auth.login(input_id=input_id, input_password=input_password)

    # 토큰 발급
    [access_token, refresh_token] = modules.auth.login_tokens(input_id)

    # token return
    response = jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    })
    set_refresh_cookies(response, refresh_token)
    return response, 200


@AuthRouter.route('/web/refresh', methods=['GET'])
@jwt_required(refresh=True, locations=["cookies"])
def webRefresh():
    identity = get_jwt_identity()
    input_refresh_token = request.cookies.get("refresh_token")

        # token 발급
    [new_access_token, new_refresh_token] = modules.auth.update_tokens(
        input_refresh_token=input_refresh_token,
        identity=identity
    )

    response = jsonify({ "access_token": new_access_token })
    set_refresh_cookies(response, new_refresh_token)
    return response, 200


@AuthRouter.route('/app/refresh', methods=['GET'])
@jwt_required(refresh=True)
def appRefresh():
    identity = get_jwt_identity()
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        input_refresh_token = auth_header.split(" ")[1]

    # token 발급
    [new_access_token, new_refresh_token] = modules.auth.update_tokens(
        input_refresh_token=input_refresh_token,
        identity=identity
    )

    response = jsonify({
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    })
    return response, 200


@AuthRouter.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    identity = get_jwt_identity()
    modules.auth.delete_tokens(user_id=identity)

    response = jsonify({
        "message": "Successfully logged out."
    })
    unset_jwt_cookies(response)

    return response, 200
