from flask import render_template

from my_app import app
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


#setup logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


@app.route("/")
def calc():
    # Zero-indexed page

    return render_template("calculator.html",
        # posts=posts,
        # has_next=has_next,
        # has_prev=has_prev,
        # page=page,
        # total_pages=total_pages
    )

@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")


@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
        author=current_user
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))


#Allows you to view a single post
@app.route("/post/<int:post_id>")
def view_post(post_id):
    post = session.query(Post)
    post = post.get(post_id + 1)
    #log.info( "post = {}".format(post) )
    return render_template("post.html",
        post=post
        )

@app.route("/post/<int:post_id>/edit", methods = ["GET"])
def edit_post(post_id):
    post = session.query(Post).get(post_id + 1)
    post_user_id = post.author_id
    post_title = post.title
    post_content = post.content

    if post_user_id == current_user.id:
        return render_template("edit_post.html",
            post_title = post_title,
            post_content = post_content
            )
    else:
        flash("You can only edit posts you have created", "danger")
        return redirect(url_for("posts"))


@app.route("/post/<int:post_id>/edit", methods = ["POST"])
def save_edit_post(post_id):
    post = session.query(Post).get(post_id + 1)
    post.title = request.form["title"]
    post.content = mistune.markdown(request.form["content"])

    #session.add(post)
    session.commit()
    return redirect(url_for("posts"))


@app.route("/post/<int:post_id>/delete", methods = ["GET"])
def delete_post(post_id):
    post = session.query(Post).get(post_id + 1)
    post_title = post.title
    return render_template("delete_post.html",
        post=post,
        post_title = post_title
        )

@app.route("/post/<int:post_id>/delete", methods = ["POST"])
def delete_post_from_db(post_id):
    post = session.query(Post).get(post_id + 1)

    if request.form["action"] == "confirm":
        session.delete(post)
        flash("Your post has been deleted", "danger")
        session.commit()
        return redirect(url_for("posts"))
    else:
        flash("Your post has not been deleted", "danger")
        return redirect(url_for("posts"))


@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("posts"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "danger")
    return redirect("/login")




