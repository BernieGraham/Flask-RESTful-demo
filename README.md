# Flask-RESTful demo

## A demonstration of a REST service using [Flask-RESTful](http://flask-restful-cn.readthedocs.org/en/latest/).
  
  
A user record is represented in JSON like:

```json
{
    "first_name": "John",
    "last_name": "Doe",
    "userid": "jdoe",
    "groups": ["groupA", "groupB"]
}
```

The following end points are implemented:  

```
GET /users/<userid>  
    Returns the matching user record or 404 if none exist.
```

```
POST /users  
    Creates a new user record. The body of the request should be a valid user
    record. POSTs to an existing user should be treated as errors and flagged
    with the appropriate HTTP status code.
```

```
DELETE /users/<userid>  
    Deletes a user record. Returns 404 if the user doesn't exist.
```

```
PUT /users/<userid>  
    Updates an existing user record. The body of the request should be a valid
    user record. PUTs to a non-existant user should return a 404.
```

```
GET /groups/<group name>  
    Returns a JSON list of userids containing the members of that group. Should
    return a 404 if the group doesn't exist.
```

```
POST /groups  
    Creates a empty group. POSTs to an existing group should be treated as
    errors and flagged with the appropriate HTTP status code. The body should contain
    a `name` parameter
```

```
PUT /groups/<group name>  
    Updates the membership list for the group. The body of the request should 
    be a JSON list describing the group's members.
```

```
DELETE /groups/<group name>  
    Deletes a group.
```

## Run
First install virtualenv (skip if already installed):  
```sh
$ pip install virtualenv
```

Clone this repository:  
```sh
$ git clone https://github.com/BernieGraham/Flask-RESTful-demo.git
$ cd Flask-RESTful-demo
```

Setup (virtual) environment:  
```sh
$ virtualenv venv  
$ source venv/bin/activate  
$ pip install -r requirements.txt
```

Run the server:  
```sh
$ ./rest.py
```

Run the tests (with the server running):  
```sh
$ ./rest_test.py
```

## Examples
Add a new user:  
```sh
$ curl -H "Content-Type: application/json" -X POST -d '{"userid":"bclinton","first_name":"Bill","last_name":"Clinton", "groups": ["presidents", "governors"]}' http://localhost:5000/users
```

Get a user:
```sh
$ curl http://localhost:5000/users/bclinton
```

Change a user:
```sh
$ curl -H "Content-Type: application/json" -X PUT -d '{"userid":"bclinton","first_name":"Hillary","last_name":"Clinton", "groups": ["senators"]}' http://localhost:5000/users/bclinton
```

Delete a user:
```sh
$ curl -X DELETE http://localhost:5000/users/bclinton
```

Add a new group:  
```sh
$ curl -X POST -d 'name=agroup' http://localhost:5000/groups
```

Get a group:
```sh
$ curl http://localhost:5000/groups/agroup
```

Change a group's membership:
```sh
$ curl -H "Content-Type: application/json" -X PUT -d '["bclinton"]' http://localhost:5000/groups/agroup
```

Delete a group:
```sh
$ curl -X DELETE http://localhost:5000/groups/agroup
```
