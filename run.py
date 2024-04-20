from flask import Flask, request
from config import DevConfig
from db import User, db
from flask_jwt_extended import create_access_token, JWTManager
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
JWTManager(app)
CORS(app)


@app.post('/signup')
def signup():
    body = request.get_json()

    new_user = User(
        username= body['username'],
        email= body['email'],
        password= body['password'],
    )

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)

    return access_token

@app.post('/login')
def login():
    body = request.get_json()

    user = User.query.filter_by(username=body['username']).first()

    if not user or str(user.password) != str(body['password']):
        return "Invalid username or password", 401

    access_token = create_access_token(identity=user.id)

    return access_token


@app.get('/')
def index():
    return "Hello, World"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
