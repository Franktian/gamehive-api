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
    uid = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    nickname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    skill = db.Column(db.Integer, nullable=False)

class Guild(db.Model):
    uid = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True, nullable=False)
    country_code = db.Column(db.String(120), unique=True, nullable=True)

class Item(db.Model):
    uid = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    skill = db.Column(db.Integer, nullable=False)

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

    # Create the player
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

@app.route('/player/update/', methods=['POST'])
def update_player():
    try:
        uid = request.json['uid']
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=400)

    # Query the player from db
    player = Player.query.filter_by(uid=uuid.UUID(uid)).first()
    if not player:
        return Response(json.dumps({
            "success": "false",
            "message": "Player {} not found".format(uid)
        }), mimetype='application/json', status=404)

    # Get info to update, if didn't find from request, don't update
    nickname = request.json.get('nickname', player.nickname)
    email = request.json.get('email', player.email)
    skill = request.json.get('skill', player.skill)

    # Update player information
    try:
        player.nickname = nickname
        player.email = email
        player.skill = skill
        db.session.commit()
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=500)

    return Response(json.dumps({
        "success": "true"
    }), mimetype='application/json')

@app.route('/player/delete/', methods=["POST"])
def delete_player():
    try:
        uid = request.json['uid']
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=400)

    # Query the player from db
    player = Player.query.filter_by(uid=uuid.UUID(uid)).first()
    if not player:
        return Response(json.dumps({
            "success": "false",
            "message": "Player {} not found".format(uid)
        }), mimetype='application/json', status=404)

    # Delete the player
    try:
        db.session.delete(player)
        db.session.commit()
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=500)

    return Response(json.dumps({
        "success": "true"
    }), mimetype='application/json')

@app.route('/guild/create/', methods=["POST"])
def create_guild():
    try:
        name = request.json['name']
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=400)

    # Create the Guild
    country_code = request.json.get('country_code', '')
    try:
        guild = Guild(
            name=name,
            country_code=country_code,
        )
        db.session.add(guild)
        db.session.commit()
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=500)

    return Response(json.dumps({
        "success": "true"
    }), mimetype='application/json')

@app.route('/guild/update/', methods=["POST"])
def update_guild():
    try:
        uid = request.json['uid']
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=400)

    # Query the guild from db
    guild = Guild.query.filter_by(uid=uuid.UUID(uid)).first()
    if not guild:
        return Response(json.dumps({
            "success": "false",
            "message": "Guild {} not found".format(uid)
        }), mimetype='application/json', status=404)

    # Get info to update, if didn't find from request, don't update
    name = request.json.get('name', guild.name)
    country_code = request.json.get('country_code', guild.country_code)

    # Update guild information
    try:
        guild.name = name
        guild.country_code = country_code
        db.session.commit()
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=500)

    return Response(json.dumps({
        "success": "true"
    }), mimetype='application/json')

@app.route('/guild/delete/', methods=["POST"])
def delete_guild():
    try:
        uid = request.json['uid']
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=400)

    # Query the player from db
    guild = Guild.query.filter_by(uid=uuid.UUID(uid)).first()
    if not guild:
        return Response(json.dumps({
            "success": "false",
            "message": "Guild {} not found".format(uid)
        }), mimetype='application/json', status=404)

    # Delete the guild
    try:
        db.session.delete(guild)
        db.session.commit()
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=500)

    return Response(json.dumps({
        "success": "true"
    }), mimetype='application/json')

@app.route('/item/create/', methods=["POST"])
def create_item():
    try:
        skill = request.json['skill']
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=400)

    # Create the item
    try:
        item = Item(
            skill=skill,
        )
        db.session.add(item)
        db.session.commit()
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=500)

    return Response(json.dumps({
        "success": "true"
    }), mimetype='application/json')

@app.route('/item/update/', methods=["POST"])
def update_item():
    try:
        uid = request.json['uid']
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=400)

    # Query the item from db
    item = Item.query.filter_by(uid=uuid.UUID(uid)).first()
    if not item:
        return Response(json.dumps({
            "success": "false",
            "message": "Item {} not found".format(uid)
        }), mimetype='application/json', status=404)

    skill = request.json.get('skill', item.skill)
    # Update item information
    try:
        item.skill = skill
        db.session.commit()
    except Exception as error:
        return Response(json.dumps({
            "success": "false",
            "message": "{}".format(error)
        }), mimetype='application/json', status=500)

    return Response(json.dumps({
        "success": "true"
    }), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
