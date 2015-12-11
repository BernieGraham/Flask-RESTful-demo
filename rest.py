#!venv/bin/python
"""
A demonstration of a REST service using Flask-RESTful.
"""

from flask import Flask, abort, request
from flask_restful import Api, Resource, reqparse, fields, marshal

app = Flask(__name__)
api = Api(app)

users = {}
groups = []

user_fields = {
    'userid': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'groups': fields.List(fields.String)
}

def upsert_groups(new_groups):
    """
    Assert that groups in given list are in the groups list
    :param new_groups:
    :return:
    """
    for new_group in new_groups:
        if new_group not in groups:
            groups.append(new_group)

def get_group_members(group):
    """
    retrieve a list of users in a given group
    :param group:
    :return:
    """
    members = []
    for user_id, user in users.iteritems():
        if group in user['groups']:
            members.append(user)
    return members

class User(Resource):
    """
    User GET, PUT, and DELETE methods
    """

    def get(self, user_id):
        """
        http GET, Returns the matching user record or 404 if none exist.
        :param user_id:
        :return:
        """

        # short circuit if there's no user
        if user_id not in users:
            abort(404, "User {} does not exists" . format(user_id))

        # success
        return users[user_id], 200

    def put(self, user_id):
        """
        http PUT, Updates an existing user record.
        :param user_id:
        :return:
        """

        # abort if there's no user to update
        if user_id not in users:
            abort(404, "User {} does not exists" . format(user_id))

         # process posted data
        user = marshal(request.get_json(), user_fields)

        # data consistency check
        if user['userid'] != user_id:
            abort(400, "Malformed request, user ID is not consistent")

        # overwrite the user in the master list
        users[user['userid']] = user

        # mark potential new groups
        if 'groups' in user:
            upsert_groups(user['groups'])

        # success
        return '', 204

    def delete(self, user_id):
        """
        http DELETE, Deletes a user record.
        :param user_id:
        :return:
        """

        # short circuit if there's no user
        if user_id not in users:
            abort(404, "User {} does not exists" . format(user_id))

        # remove from dictionary
        del users[user_id]

        # success
        return '', 204

class NewUser(Resource):

    def post(self):
        """
        http POST, Creates a new user record.
        :return:
        """

        # process posted data
        user = marshal(request.get_json(), user_fields)

        # check for completeness
        if 'userid' not in user:
            abort(400, "Incomplete User object supplied")

        # short circuit if the user is already in the system
        if user['userid'] in users:
            abort(409, "User: {} already exists" . format(user['userid']))

        # add the new user to the list
        users[user['userid']] = user

        # mark potential new groups
        if 'groups' in user:
            upsert_groups(user['groups'])

        # success
        return '', 204

class Group(Resource):
    """
    Group GET, PUT, and DELETE methods
    """

    def get(self, group_name):
        """
        http GET, Returns a JSON list of userids containing the members of that group.
        :param group_name:
        :return:
        """

        # abort if there's no group
        if group_name not in groups:
            abort(404, "Group {} does not exists" . format(group_name))

        # success
        return get_group_members(group_name), 200

    # http PUT, Updates the membership list for the group.
    def put(self, group_name):
        """
        http PUT, Updates the membership list for the group.
        :param group_name:
        :return:
        """
        # make sure the group exists
        upsert_groups([group_name])

        # read the data supplied
        members = request.get_json()

        # make sure input is only strings
        for member in members:
            if not isinstance(member, basestring):
                abort(404, "Only a list of member IDs is allowed")

        # go through all the users and add or remove group membership accordingly
        for user_id, user in users.iteritems():
            if user_id in members:
                if group_name not in user['groups']:
                    user['groups'].append(group_name)
            else:
                if group_name in user['groups']:
                    user['group'].remove(group_name)

        return '', 204

    def delete(self, group_name):
        """
        http DELETE, Deletes a group.
        :param group_name:
        :return:
        """

        # short circuit if there's no group
        if group_name not in groups:
            abort(404, "Group {} does not exists" . format(group_name))

        # remove from group list
        groups.remove(group_name)

        # remove all groups memebership
        for user_id, user in users.iteritems():
            if group_name in user['groups']:
                user['groups'].remove(group_name)

        # success
        return '', 204

class NewGroup(Resource):
    """
    http POST, Creates a empty group.
    """
    def post(self):
        """
        http POST, Creates a new group.
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        group_name = args['name']

        # short circuit if the group is already in the list
        if group_name in groups:
            abort(409, "Group: {} already exists" . format(group_name))

        # add group to the list
        groups.append(group_name)

        return '', 204

# users routes
api.add_resource(User, '/users/<string:user_id>')
api.add_resource(NewUser, '/users')

# groups routs
api.add_resource(Group, '/groups/<string:group_name>')
api.add_resource(NewGroup, '/groups')

if __name__ == '__main__':
    app.run(debug=True)
