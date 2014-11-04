from flask import Blueprint, request, url_for, make_response, abort
from service.api import AuthNZ_APC_API, NoSuchRecordException
import json

blueprint = Blueprint('api', __name__,)

@blueprint.route('/apc', methods=["POST"])
def create():
    api_key = request.values.get("api_key")
    local_id = request.headers.get("slug")
    data = request.get_json()  # FIXME: might not be in this version of flask

    # FIXME: at this stage, we don't bother with the account
    ir = AuthNZ_APC_API.create(data, local_id=local_id, account=api_key)

    location = url_for("api.apc", apc_id=ir.id)
    ro = {
        "status" : 201,
        "location" : location,
    }

    if ir.local_id is not None:
        local = url_for("api.retrieve_local", local_id=ir.local_id)
        ro["local"] = local

    resp = make_response(json.dumps(ro))
    resp.mimetype = "application/json"
    resp.headers["Location"] = location
    resp.status_code = 201
    return resp

@blueprint.route('/apc/<apc_id>', methods=["GET", "PUT", "DELETE"])
def apc(apc_id):
    if request.method == "GET":
        try:
            ir = AuthNZ_APC_API.retrieve(apc_id)
        except NoSuchRecordException:
            abort(404)
        j = ir.json()
        resp = make_response(j)
        resp.mimetype = "application/json"
        return resp

    elif request.method == "PUT":
        api_key = request.values.get("api_key")
        local_id = request.headers.get("slug")
        data = request.get_json()  # FIXME: might not be in this version of flask

        # FIXME: at this stage, we don't bother with the account
        try:
            ir = AuthNZ_APC_API.create(apc_id, data, local_id=local_id, account=api_key)
        except NoSuchRecordException:
            abort(404)

        # FIXME: is this how you return a No Content?
        return 204

    elif request.method == "DELETE":
        api_key = request.values.get("api_key")
        try:
            # FIXME: we don't use the account at this stage
            ir = AuthNZ_APC_API.delete(apc_id, account=api_key)
        except NoSuchRecordException:
            abort(404)

        # FIXME: is this how you return a No Content?
        return 204

@blueprint.route("/local/<local_id>", methods=["GET"])
def retrieve_local(local_id):
    try:
        ir = AuthNZ_APC_API.retrieve_by_local_id(local_id)
    except NoSuchRecordException:
        abort(404)
    j = ir.json()
    resp = make_response(j)
    resp.mimetype = "application/json"
    return resp
