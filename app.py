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
@app.route("/dishes_list")
def dishes_list():
    dishes = list(mongo.db.dishes.find())
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

        register_user = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register_user)

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
        dishes = list(mongo.db.dishes.find())
        return render_template(
            "profile.html", username=username, dishes=dishes)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.clear()
    return redirect(url_for("login"))


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    dishes = list(mongo.db.dishes.find({"$text": {"$search": query}}))
    return render_template(
        "profile.html", username=session["user"], dishes=dishes)


@app.route("/recipe/<recipe_id>")
def individual_recipe(recipe_id):
    # grab recipe name from database
    recipe = mongo.db.dishes.find_one({"_id": ObjectId(recipe_id)})
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
            "recipe": request.form.get("recipe"),
            "equipment": request.form.get("equipment"),
            "description": request.form.get("description"),
            "image": request.form.get("image"),
            "created_by": session["user"]
        }
        mongo.db.dishes.insert_one(dish)
        flash("Dish Successfully Added")
        return redirect(url_for("profile", username=session["user"]))
    dishes = mongo.db.dishes.find()
    categories = mongo.db.categories.find().sort("region")

    return render_template(
        "add_recipe.html", dishes=dishes, categories=categories)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        dish = {
            "region": request.form.get("region"),
            "dish_name": request.form.get("dish_name"),
            # n.b. here for ingredients, user could create a list of 
            # ingredients in the form (one at a time),
            # and then use request.form.getlist() here
            "ingredients": request.form.get("ingredients"),
            "recipe": request.form.get("recipe"),
            "equipment": request.form.get("equipment"),
            "description": request.form.get("description"),
            "image": request.form.get("image"),
            "created_by": session["user"]
        }
        mongo.db.dishes.update({"_id": ObjectId(recipe_id)}, dish)
        flash("Dish Successfully Updated")
        return redirect(url_for("profile", username=session["user"]))

    recipe = mongo.db.dishes.find_one({"_id": ObjectId(recipe_id)})

    categories = mongo.db.categories.find().sort("region")
    return render_template(
        "edit_recipe.html", recipe=recipe, categories=categories)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.dishes.remove({"_id": ObjectId(recipe_id)})
    flash("Dish Successfully Removed")
    return redirect(url_for("profile", username=session["user"]))



@app.route("/manage_category")
def manage_category():
    categories = list(mongo.db.categories.find())
    return render_template("manage_category.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "region": request.form.get("region")
        }
        mongo.db.categories.insert_one(category)
        flash("New Region Added")
        return redirect(url_for("manage_category"))
    return render_template("add_category.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "region": request.form.get("region")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
        flash("Region Successfully Updated")
        return redirect(url_for('manage_category'))
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
