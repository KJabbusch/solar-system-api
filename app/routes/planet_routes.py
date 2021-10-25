from flask import Blueprint, jsonify, request, make_response
from app import db
from app.planets_class import Planet
from app.load_json import load
import pprint

# loads json data as dictionaries
planet_data = load('app/planets.json')

planet_schema = {
    "key-values":
        {
        "name": {"type", "string"},
        "description": {"type", "string"},
        "num_of_moons": {"type", "integer"},
    },
    "required": ["name", "description", "num_of_moons"]
}

def validate_json(json_data):
    try:
        validate(instance=json_data, schema=planet_schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

def make_planet_objects():
    planets_list = []

    for planet in planet_data:
        description = f'{planet["name"]} is the {planet["id"]} planet and has {planet["numberOfMoons"]} moon(s).'
        planet_object = Planet(planet["id"], planet["name"], description, planet["numberOfMoons"])
        planets_list.append(planet_object)

    return planets_list

planets = make_planet_objects()

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("/", methods=["POST"])
def handle_planets():
    request_body = request.get_json()
    new_planet = Planet(
        name = request_body.name,
        description = request_body.description,
        num_of_moons= request_body.num_of_moons,
    )
    db.session.add(new_planet)
    db.session.commit()

    return make_response("sdfgkhdfg")



@planets_bp.route("/", methods=["GET"])
def handle_planets():
    planets_response = []
    
    for planet in planets:
        planets_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "num_of_moons": planet.num_of_moons
            })
    return jsonify(planets_response)


@planets_bp.route("/<planet_id>", methods=["GET"])
def handle_planet(planet_id):
    planet_id = int(planet_id)

    planet_response = {}

    for planet in planets:
        if planet_id == planet.id:
            planet_response["id"] = planet.id
            planet_response["name"] = planet.name
            planet_response["description"] = planet.description
            planet_response["num_of_moons"] = planet.num_of_moons
            
    return jsonify(planet_response)