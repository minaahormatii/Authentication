from flask import Blueprint

import controllers

org = Blueprint("org", __name__)


@org.route("/organization", methods=['POST'])
def add_org():
    return controllers.add_org()

@org.route("/organizations", methods=['GET'])
def get_all_orgs():
    return controllers.get_all_orgs()
    