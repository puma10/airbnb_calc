post_schema = {
    "properties": {
        "title" : {"type" : "string"},
        "rent": {"type" : "integer"}
    },
    "required": ["title", "rent"]
}

from flask import render_template
import json
from flask import request, Response, url_for

from my_app import app, decorators
from database import session
from models import User, Input, Output

from flask import request, redirect, url_for

from flask import flash
from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from models import User
from flask.ext.login import login_required
from flask.ext.login import current_user
from flask.ext.login import logout_user
from jsonschema import validate, ValidationError


#setup logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


@app.route("/api", methods=["GET", "POST"])
@decorators.accept("application/json")
def calc():
    if request.method == 'POST':
        form_title = request.form["title"]

    # Get the input posted to the database
    input_posts = session.query(Input).all()

    # Convert the posts to JSON and return a response
    data = json.dumps([input_post.as_dictionary() for input_post in input_posts])
    return Response(data, 200, mimetype="application/json")


@app.route("/api/posts/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def post_get(id):
    """ Single post endpoint """
    # Get the post from the database
    input_post = session.query(Input).get(id)

    # Check whether the input_post exists
    # If not return a 404 with a helpful message
    # This if not means if input_post does not exist
    if not input_post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # Return the post as JSON
    data = json.dumps(input_post.as_dictionary())
    return Response(data, 200, mimetype="application/json")


@app.route("/api/posts", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
def posts_post():
    """ Add a new post """
    data = request.json

    # Check that the JSON supplied is valid
    # If not we return a 422 Unprocessable Entity
    try:
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")

    # Add the post to the database
    post = Input(title=data["title"], rent=data["rent"])
    session.add(post)
    session.commit()

    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    data = json.dumps(post.as_dictionary())
    headers = {"Location": url_for("post_get", id=post.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")


