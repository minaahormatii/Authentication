from flask import Blueprint

import controllers

search = Blueprint("search", __name__)


@search.route("/users/search", methods=["GET"])
def users_get_by_search():
    return controllers.users_get_by_search()