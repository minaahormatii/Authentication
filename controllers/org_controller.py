from flask import jsonify, request

from db import db
from lib.authenticate import authenticate
from models.organization import Organizations, org_schema, orgs_schema
from util.reflection import populate_object


def add_org():
    post_data = request.form if request.form else request.get_json()

    new_org = Organizations.new_org_obj()

    populate_object(new_org, post_data)

    
    db.session.add(new_org)
    db.session.commit()


    return jsonify({"message": "org created", "result": org_schema.dump(new_org)}), 201

@authenticate
def get_all_orgs():
    orgs_query = db.session.query(Organizations).all()

    return jsonify({"message": "organizations found", "results": orgs_schema.dump(orgs_query)}), 200
    