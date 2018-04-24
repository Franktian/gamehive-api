from flask import Flask, request, Response, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import UUIDType
import uuid

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://gamehive:gamehive@postgres:5432/gamehive'

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    skill = db.Column(db.Integer, nullable=False)

class Guild(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    country_code = db.Column(db.String(120), unique=True, nullable=True)

@app.route('/')
def root():
    return 'Game Hive Player API'

@app.route('/player/create/', methods=['POST'])
def create_player():
    try:
        nickname = request.json['nickname']
        email = request.json['email']
        skill = request.json['skill']
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=400)

    try:
        player = Player(
            nickname=nickname,
            email=email,
            skill=skill
        )
        db.session.add(player)
        db.session.commit()
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=500)

    return Response(json.dumps({
        "success": "true"
    }), mimetype='application/json', status=200)

@app.route('/player/update/')
def update_player():
    return Response(json.dumps({
        "success": "true"
    }), mimetype='application/json')

@app.route('/player/delete/')
def delete_player():
    return Response(json.dumps({
        "success": "true"
    }), mimetype='application/json')

@app.route('/guild/create/')
def create_guild():
    return Response(json.dumps({
        "success": "true"
    }), mimetype='application/json')

@app.route('/guild/update/')
def update_guild():
    return Response(json.dumps({
        "success": "true"
    }), mimetype='application/json')

@app.route('/guild/delete/')
def delete_guild():
    return Response(json.dumps({
        "success": "true"
    }), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
