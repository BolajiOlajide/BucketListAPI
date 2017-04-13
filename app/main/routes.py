"""
This script contains the routes for the different API methods.

This handles the overall routing of the application.
"""
from datetime import datetime

from flask import g, jsonify, request

from . import main
from app import db, errors
from app.auth.routes import auth
from app.decorators import json, paginate
from app.models import BucketList, Items
import sqlalchemy


@main.route('/bucketlists/', methods=['GET'])
@auth.login_required
@paginate()
def get_bucketlists():
    """
    List all the created BucketLists.

    Displays a json of all the created BucketLists and the various items
    associated with them.
    """
    if request.args.get('q'):
        return BucketList.query.filter_by(created_by=g.user.user_id).filter(
            BucketList.name.contains(request.args.get('q')))
    else:
        return BucketList.query.filter_by(created_by=g.user.user_id)


@main.route('/bucketlists/<int:list_id>', methods=['GET'])
@auth.login_required
@json
def get_bucketlist(list_id):
    """
    Get single bucket list.

    Return a json of all the information as regards a particular BucketList.
    """
    bucketlist = BucketList.query.filter_by(bucketlist_id=list_id).first()
    if not bucketlist or bucketlist.created_by != g.user.user_id:
        return errors.not_found("The BucketList with the id: {0} doesn't"
                                " exist.".format(list_id))
    return bucketlist, 200


@main.route('/bucketlists/', methods=['POST'], strict_slashes=False)
@auth.login_required
@json
def create_bucketlist():
    """
    Create a new BucketList.

    Add a new bucketlist and returns the bucketlist for the user to view
    """
    if not request.json or 'name' not in request.json:
        return errors.bad_request("Only JSON object is accepted. Please "
                                  "confirm that the key 'name' exists.")

    try:
        bucketlist = BucketList(
            name=request.json.get('name'),
            created_by=g.user.user_id
        )
        bucketlist.save()
    except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.InvalidRequestError):
        db.session().rollback()
        return errors.bad_request(
            "A BucketList with the name {0} exists.".format(
                request.json.get('name')))
    return bucketlist, 201


@main.route('/bucketlists/<int:list_id>', methods=['PUT'])
@auth.login_required
@json
def update_bucketlist(list_id):
    """
    Update BucketList.

    Update a BucketList name.
    """
    if not request.json:
        return errors.bad_request("Invalid Input. Only JSON input is allowed.")
    elif 'name' not in request.json:
        return errors.bad_request("The key 'name' not in the JSON")
    else:
        bucketlist = BucketList.query.filter_by(bucketlist_id=list_id).first()

        if not bucketlist or bucketlist.created_by != g.user.user_id:
            return errors.not_found("The BucketList with the id: {0} doesn't"
                                    " exist.".format(list_id))
        else:
            bucketlist.name = request.json.get('name')
            bucketlist.save()
            return bucketlist, 200


@main.route('/bucketlists/<int:list_id>', methods=['DELETE'])
@auth.login_required
def delete_bucketlist(list_id):
    """
    Delete a BucketList.

    Deletes a BucketList and all items associated with it.
    """
    bucketlist = BucketList.query.filter_by(bucketlist_id=list_id).first()

    if not bucketlist or bucketlist.created_by != g.user.user_id:
        return errors.not_found("The BucketList with the id: {0} doesn't"
                                " exist.".format(list_id))
    else:
        bucketlist.delete()
        return jsonify({'Delete': True}), 200


@main.route(
    '/bucketlists/<int:list_id>/items/', methods=['POST'], strict_slashes=False
)
@auth.login_required
@json
def add_bucketlist_item(list_id):
    """
    Add new item.

    This function adds a new item to a BucketList. It gets the name and done
    keys from the json supplied and saves to the database.
    """
    bucketlist = BucketList.query.filter_by(bucketlist_id=list_id).first()

    if not bucketlist or bucketlist.created_by != g.user.user_id:
        return errors.not_found("The BucketList with the id: {0} doesn't"
                                " exist.".format(list_id))

    if not request.json or (('name' or 'done') not in request.json):
        return errors.bad_request("Only JSON object is accepted.Please confirm"
                                  " that the key 'name' or 'done' exists.")

    item = Items().from_json(request.json)
    item.bucketlist_id = bucketlist.bucketlist_id
    item.save()
    return bucketlist, 201


@main.route(
    '/bucketlists/<int:list_id>/items/<int:item_id>', methods=['PUT']
)
@auth.login_required
@json
def update_bucketlist_item(list_id, item_id):
    """
    Update item.

    This function updates an item in a BucketList.
    """
    bucketlist = BucketList.query.filter_by(bucketlist_id=list_id).first()

    if not bucketlist or bucketlist.created_by != g.user.user_id:
        return errors.not_found("The BucketList with the id: {0} doesn't"
                                " exist.".format(list_id))

    item = Items.query.get(item_id)
    if not item or (item.bucketlist_id != bucketlist.bucketlist_id):
        return errors.not_found("The item with the ID: {0} doesn't exist"
                                .format(item_id))

    if not request.json:
        return errors.bad_request("Invalid Input. Only JSON input is allowed.")
    elif ('name' or 'done') not in request.json:
        return errors.bad_request(
            "The key 'name' or 'done' cannot be found in the JSON provided.")
    else:
        item.name = request.json.get('name')
        item.done = request.json.get('done')
        item.save()
        return bucketlist, 200


@main.route(
    '/bucketlists/<int:list_id>/items/<int:item_id>', methods=['DELETE']
)
@auth.login_required
@json
def delete_bucketlist_item(list_id, item_id):
    """
    Delete an item.

    This function deletes an item from a BucketList.
    """
    bucketlist = BucketList.query.filter_by(bucketlist_id=list_id).first()
    item = Items.query.filter_by(item_id=item_id).first()

    if not bucketlist or bucketlist.created_by != g.user.user_id:
        return errors.not_found("The BucketList with the id: {0} doesn't"
                                " exist.".format(list_id))
    elif not item or (item.bucketlist_id != bucketlist.bucketlist_id):
        return errors.not_found("The item with the ID: {0} doesn't exist"
                                .format(item_id))
    else:
        item.delete()
        return bucketlist, 200


@main.route('/login', methods=["POST"], strict_slashes=False)
def login2():
    """
    Secure redundant route.

    Protect the route: /login from being accessed by the end user.
    """
    return errors.not_found("The page doesn't exist")


@main.route('/register', methods=["POST"], strict_slashes=False)
def register_user2():
    """
    Secure redundant route.

    Protect the route: /register from being accessed by the end user.
    """
    return errors.not_found("The Page doesn't exist")
