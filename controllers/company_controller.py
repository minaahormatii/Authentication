from flask import jsonify, request

from db import db
from lib.authenticate import authenticate_return_auth
from models.product import Products, product_schema, products_schema
from models.company import Companies, company_schema, companies_schema
from util.reflection import populate_object


@authenticate_return_auth
def add_company(auth_info):
    post_data = request.form if request.form else request.get_json()

    if auth_info.user.role == "super-admin":

        new_company = Companies.new_company_obj()
        populate_object(new_company, post_data)

        db.session.add(new_company)
        db.session.commit()

        return jsonify({"message": "company created", "result": company_schema.dump(new_company)}), 201

    return jsonify({"message": "invalid permisssion"}), 403


def get_all_companies():
    company_query = db.session.query(Companies).all()

    return jsonify({"message": "companies found", "results": companies_schema.dump(company_query)}), 200


@authenticate_return_auth
def update_company_by_id(company_id, auth_info):
    post_data = request.form if request.form else request.get_json()
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if auth_info.user.role == "super-admin":

        if company_query:
            populate_object(company_query, post_data)

            db.session.commit()
            return jsonify({"message": "company updated", "result": company_schema.dump(company_query)}), 200
        
        return jsonify({"message": "company not found"}), 404

    return jsonify({"message": "invalid permisssion"}), 403


def get_company_by_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "company not found"}), 404

    return jsonify({"message": "company found", "result": company_schema.dump(company_query)}), 200


@authenticate_return_auth
def delete_company_by_id(company_id, auth_info):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    

    if not company_query:
        return jsonify({"message": "company not found"}), 404

    if auth_info.user.role == "super-admin":

        try:
            db.session.delete(company_query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete company"}), 400

        return jsonify({"message": "company deleted"}), 200

    return jsonify({"message": "invalid permisssion"}), 403