#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

import os

abs_path=os.getcwd()

db_path=f'sqlite:///{abs_path}/db/app.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

# @app.route('/add-dumy')
# def add_dummy():
#     hero=Hero(name='Leo',super_name='belligoal')
#     db.session.add(hero)
#     db.session.commit()

#     return 'Hero added'

@app.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [
        {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
        for hero in heroes
    ]
    return jsonify(heroes_data)


@app.route("/heroes/<int:hero_id>", methods=["GET"])
def get_hero_by_id(hero_id):
    hero = Hero.query.get(hero_id)

    if hero:
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {"id": power.id, "name": power.name, "description": power.description}
                for power in hero.powers
            ]
            if hasattr(hero, "powers")
            else [],
        }
        return jsonify(hero_data)
    else:
        return make_response(jsonify({"error": "not found"}), 401)
    

    
@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    powers_data = [
        {"id": power.id, "name": power.name, "description": power.description}
        for power in powers
    ]
    return jsonify(powers_data)



@app.route("/powers/<int:power_id>", methods=["GET", "PATCH"])
def get_or_update_power(power_id):
    power = Power.query.get(power_id)

    if not power:
        return make_response(jsonify({"error": "Power not found"}), 404)

    if request.method == "GET":
        power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
        }
        return jsonify(power_data)
    elif request.method == "PATCH":
        data = request.get_json()

        if "description" in data:
            power.description = data["description"]
            db.session.commit()
            updated_power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
            }
            return jsonify(updated_power_data)
        else:
            return make_response(
                jsonify({"errors": ["unavailable 'description' in request"]}), 401
            )

    





if __name__ == '__main__':
    app.run(port=3000,debug = True )



