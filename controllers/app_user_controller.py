from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from lib.authenticate import authenticate_return_auth
from models.app_user import AppUsers, user_schema, users_schema
from models.organization import Organizations
from util.reflection import populate_object


def add_user():
    post_data = request.form if request.form else request.json
    org_id = post_data.get("org_id")

    if not org_id:
        return jsonify({"message": "org_id is required"}), 400

    org_query = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()

    if not org_query:
        return jsonify({"message": "org not found"}), 404

    new_user = AppUsers.new_user_obj()

    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode("utf8")

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user created", "result": user_schema.dump(new_user)}), 201

@authenticate_return_auth
def user_get_all(auth_info):
    if auth_info.user.role != "super-admin":
        return jsonify({"message": "invalid permissions"}), 403
    
    users_query = db.session.query(AppUsers).all()

    return jsonify({"message": "users found", "results": users_schema.dump(users_query)}), 200


@authenticate_return_auth
def user_get_by_id(user_id, auth_info):

    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404
    
    if auth_info.user.role == "super-admin" or str(auth_info.user.user_id) == user_id:

        return jsonify({"message": "user found", "result": user_schema.dump(user_query)}), 200


    return jsonify({"message": "invalid permissions"}), 403

@authenticate_return_auth
def user_update_by_id(user_id, auth_info):

    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404
    
    if auth_info.user.role == "super-admin" or str(auth_info.user.user_id) == user_id:

        post_data = request.form if request.form else request.json

        populate_object(user_query, post_data)

        db.session.commit()

        return jsonify({"message": "user updated", "result": user_schema.dump(user_query)}), 200


    return jsonify({"message": "invalid permissions"}), 403

@authenticate_return_auth
def user_delete_by_id(user_id, auth_info):

    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404
    
    if auth_info.user.role == "super-admin" or str(auth_info.user.user_id) == user_id:

        db.session.delete(user_query)
        db.session.commit()

        return jsonify({"message": "user deleted"}), 200


    return jsonify({"message": "invalid permissions"}), 403