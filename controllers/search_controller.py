from flask import jsonify, request

from db import db
from lib.authenticate import authenticate
from models.app_user import AppUsers, users_schema


@authenticate
def users_get_by_search():
    search_term = request.args.get("q")

    if not search_term:
        return jsonify({"message": "search term q is required"}), 400

    search_term = search_term.lower()

    users_query = (
        db.session.query(AppUsers)
        .filter(
            db.or_(
                db.func.lower(AppUsers.first_name).contains(search_term),
                db.func.lower(AppUsers.last_name).contains(search_term),
                db.func.lower(AppUsers.email).contains(search_term),
            )
        )
        .order_by(AppUsers.last_name.asc())
        .all()
    )

    return jsonify({"message": "users found", "results": users_schema.dump(users_query)}), 200