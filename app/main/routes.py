"""
This script contains the routes for the different API methods.

This handles the overall routing of the application.
"""
from flask import abort, jsonify, request

from . import main
from app import errors
from app.decorators import json, paginate
from app.models import BucketList, Items, User


@main.route('/bucketlists', methods=['GET'])
@paginate()
def get_bucketlists():
    """
    List all the created BucketLists.

    Displays a json of all the created BucketLists and the various items
    associated with them.
    """
    if not BucketList.query.all():
        return errors.not_found("You currently have no BucketList saved.")

    bucketlists = []

    user = User.query.filter_by(username='andela').first().user_id

    if request.args.get('q'):
        try:
            result = BucketList.query.filter_by(created_by=user).filter(
                BucketList.name.contains(request.args.get('q'))).first()
        except:
            return errors.not_found(
                "No BucketList exist with the name {}"
                .format(request.args.get('q'))
            )
        finally:
            bucketlists = result.to_json()
            return jsonify({'bucketlist': bucketlists}), 200
    else:
        return BucketList.query.filter_by(created_by=user)


@main.route('/bucketlists/<int:list_id>', methods=['GET'])
@json
def get_bucketlist(list_id):
    """
    Get single bucket list.

    Return a json of all the information as regards a particular BucketList.
    """
    bucketlist = BucketList.query.filter_by(bucketlist_id=list_id).first()
    if not bucketlist:
        return errors.not_found("The BucketList with the id: {0} doesn't"
                                " exist.".format(list_id))
    return bucketlist, 200


@main.route('/bucketlists/', methods=['POST'])
@json
def create_bucketlist():
    """
    Create a new BucketList.

    Add a new bucketlist and returns the bucketlist for the user to view
    """
    if not request.json or 'name' not in request.json:
        return errors.bad_request("Only JSON object is accepted. Please "
                                  "confirm that the key 'name' exists.")

    user = User.query.filter_by(username='andela').first().user_id
    try:
        bucketlist = BucketList(name=request.json.get('name'), created_by=user)
        bucketlist.save()
    except:
        return errors.bad_request("An error occurred while saving. "
                                  "Please try again.")
    return bucketlist, 201


@main.route('/bucketlists/<int:list_id>', methods=['PUT'])
@json
def update_bucketlist(list_id):
    """
    Update BucketList.

    Update a BucketList name.
    """
    bucketlist = BucketList.query.get_or_404(list_id)

    if not request.json:
        abort(400)

    if 'done' not in request.json or 'name' not in request.json:
        abort(400)

    if type(request.json['name']) != unicode:
        abort(400)

    bucketlist.name = request.json.get('name')
    bucketlist.save()
    return bucketlist, 200


@main.route('/bucketlists/<int:list_id>', methods=['DELETE'])
def delete_bucketlist(list_id):
    """
    Delete a BucketList.

    Deletes a BucketList and all items associated with it.
    """
    bucketlist = BucketList.query.get_or_404(list_id)

    if not bucketlist:
        abort(404)

    bucketlist.delete()
    return jsonify({'Delete': True}), 200


@main.route('/bucketlists/<int:list_id>/items/', methods=['POST'])
@json
def add_bucketlist_item(list_id):
    """
    Add new item.

    This function adds a new item to a BucketList. It gets the name and done
    keys from the json supplied and saves to the database.
    """
    bucketlist = BucketList.query.get_or_404(list_id)
    if not request.json or 'name' not in request.json:
        abort(400)

    item = Items().from_json(request.json)
    item.bucketlist_id = bucketlist.bucketlist_id
    item.save()
    return bucketlist, 201


@main.route(
    '/bucketlists/<int:list_id>/items/<int:item_id>', methods=['PUT']
)
@json
def update_bucketlist_item(list_id, item_id):
    """
    Update item.

    This function updates an item in a BucketList.
    """
    bucketlist = BucketList.query.get_or_404(list_id)
    item = Items.query.get_or_404(item_id)

    if not request.json:
        abort(400)

    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)

    item.name = request.json.get('name')
    item.done = request.json.get('done')
    item.save()
    return bucketlist, 200


@main.route(
    '/bucketlists/<int:list_id>/items/<int:item_id>', methods=['DELETE']
)
@json
def delete_bucketlist_item(list_id, item_id):
    """
    Delete an item.

    This function deletes an item from a BucketList.
    """
    bucketlist = BucketList.query.get_or_404(list_id)
    item = Items.query.get_or_404(item_id)

    if item.bucketlist_id != bucketlist.bucketlist_id:
        abort(500)

    item.delete()
    return bucketlist, 200


@main.route('/login', methods=["POST", "GET"])
def login2():
    """
    Secure redundant route.

    Protect the route: /login from being accessed by the end user.
    """
    return jsonify({"message": "Page not allowed."}), 404


@main.route('/register')
def register_user2():
    """
    Secure redundant route.

    Protect the route: /register from being accessed by the end user.
    """
    return jsonify({"message": "Page not allowed."}), 404
