from flask import jsonify, request

from db import db
from lib.authenticate import authenticate_return_auth
from models.product import Products
from models.warranty import Warranties, warranty_schema, warranties_schema
from util.reflection import populate_object



@authenticate_return_auth
def add_warranty(auth_info):
    post_data = request.form if request.form else request.json

    if auth_info.user.role == "super-admin":

        new_warranty = Warranties.new_warranty_obj()
        populate_object(new_warranty, post_data)

        db.session.add(new_warranty)
        db.session.commit()

        return jsonify({"message": "warranty created", "result": warranty_schema.dump(new_warranty)}), 201

    return jsonify({"message": "invalid permission"}), 403


def get_warranty_by_id(warranty_id):
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": "warranty not found"}), 404

    return jsonify({"message": "warranty found", "result": warranty_schema.dump(warranty_query)}), 200


@authenticate_return_auth
def update_warranty_by_id(warranty_id, auth_info):
    post_data = request.form if request.form else request.json
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if auth_info.user.role == "super-admin":

        if warranty_query:
            populate_object(warranty_query, post_data)

            db.session.commit()
            return jsonify({"message": "warranty updated", "result": warranty_schema.dump(warranty_query)}), 200

        return jsonify({"message": "warranty not found"}), 404

    return jsonify({"message": "invalid permission"}), 403


@authenticate_return_auth
def delete_warranty_by_id(warranty_id, auth_info):
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": "warranty not found"}), 404

    if auth_info.user.role == "super-admin":

        try:
            db.session.delete(warranty_query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete warranty"}), 400

        return jsonify({"message": "warranty deleted"}), 200

    return jsonify({"message": "invalid permission"}), 403