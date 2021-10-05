import os
from flask import (
    Flask, flash, render_template, redirect, 
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/dishes")
def dishes():
    dishes = mongo.db.dishes.find()
    return render_template("dishes.html", dishes=dishes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username Already Exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure password input matches hashed, saved password
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                        request.form.get("username")))
                return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username/ Password")
                return redirect(url_for("login"))
        else:
            # username doesn't exist
            flash("Incorrect Username/ Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab session user's username from database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        dishes = mongo.db.dishes.find()
        return render_template(
            "profile.html", username=username, dishes=dishes)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.clear()
    return redirect(url_for("login"))


@app.route("/recipe/<recipe_id>")
def individual_recipe(recipe_id):
    # grab recipe name from database
    recipe = mongo.db.dishes.find_one({"_id": ObjectId(recipe_id)})
    print(recipe_id)
    print(recipe)
    return render_template(
        "individual_recipe.html", recipe=recipe)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        dish = {
            "region": request.form.get("region"),
            "dish_name": request.form.get("dish_name"),
            # n.b. here for ingredients, user could create a list of 
            # ingredients in the form (one at a time),
            # and then use request.form.getlist() here
            "ingredients": request.form.get("ingredients"),
            "equipment": request.form.get("equipment"),
            "description": request.form.get("description"),
            "image": request.form.get("image"),
            "created_by": session["user"]
        }
        mongo.db.dishes.insert_one(dish)
        return redirect(url_for("dishes"))
        flash("Dish Successfully Added")
    dishes = mongo.db.dishes.find()
    categories = mongo.db.categories.find().sort("region")

    return render_template(
        "add_recipe.html", dishes=dishes, categories=categories)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = mongo.db.dishes.find_one({"_id": ObjectId(recipe_id)})

    categories = mongo.db.categories.find().sort("region")
    return render_template(
        "edit_task.html", recipe=recipe, categories=categories)



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
