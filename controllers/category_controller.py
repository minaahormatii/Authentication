from flask import jsonify, request

from db import db
from lib.authenticate import authenticate_return_auth
from models.product import Products
from models.category import Categories, category_schema, categories_schema
from util.reflection import populate_object


@authenticate_return_auth
def add_category(auth_info):
    post_data = request.form if request.form else request.json

    if auth_info.user.role == "super-admin":

        new_category = Categories.new_category_obj()
        populate_object(new_category, post_data)

        db.session.add(new_category)
        db.session.commit()


        return jsonify({"message": "category created", "result": category_schema.dump(new_category)}), 201

    return jsonify({"message": "invalid permission"}), 403


def get_all_categories():
    category_query = db.session.query(Categories).all()

    return jsonify({"message": "categories found", "results": categories_schema.dump(category_query)}), 200


@authenticate_return_auth
def update_category_by_id(category_id, auth_info):
    post_data = request.form if request.form else request.json
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if auth_info.user.role == "super-admin":

        if category_query:
            populate_object(category_query, post_data)

            db.session.commit()
            return jsonify({"message": "category updated", "result": category_schema.dump(category_query)}), 200

        return jsonify({"message": "category not found"}), 404

    return jsonify({"message": "invalid permission"}), 403


def get_category_by_id(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": "category not found"}), 404

    return jsonify({"message": "category found", "result": category_schema.dump(category_query)}), 200


@authenticate_return_auth
def delete_category_by_id(category_id, auth_info):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()


    if not category_query:
        return jsonify({"message": f"category does not exist"}), 404

    if auth_info.user.role == "super-admin":

        try:
            db.session.delete(category_query)
            db.session.commit()

        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete category"}), 400

        return jsonify({"message": "category deleted"}), 200

    return jsonify({"message": "invalid permission"}), 403