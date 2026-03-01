import os
from flask import Flask
from datetime import timedelta
from flask_jwt_extended import JWTManager
from router.auth import AuthRouter
from router.user import UserRouter
from router.set import SetRouter
from router.word import WordRouter
from errors.errors import register_error_handlers
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

register_error_handlers(app)

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=60)
app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"
app.json.ensure_ascii = False
app.json.sort_keys = False

jwt = JWTManager(app)


@app.route('/', methods=['GET'])
def welcome():
    return "welcome to word not api", 200

app.register_blueprint(AuthRouter, url_prefix='/auth')
app.register_blueprint(UserRouter, url_prefix='/user')
app.register_blueprint(SetRouter, url_prefix='/set')
app.register_blueprint(WordRouter, url_prefix='/words')

if __name__ == '__main__':
    app.run()
