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
    """ Homepage for users not logged in """
    dishes = list(mongo.db.dishes.find())
    return render_template("dishes.html", dishes=dishes)


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Allows user to register to personalise website """
    if request.method == "POST":
        """ check if username already exists in database """
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
        """ put new user into 'session' cookie """
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Allows user to login to their saved profile """
    if request.method == "POST":
        """ check if username exists in database """
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            """ ensure password input matches hashed, saved password """
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                        request.form.get("username")))
                return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                """ invalid password match """
                flash("Incorrect Username/ Password")
                return redirect(url_for("login"))
        else:
            """ username doesn't exist """
            flash("Incorrect Username/ Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """ grab session user's username from database """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    """ Display user's home profile page """
    if session["user"]:
        dishes = list(mongo.db.dishes.find())
        return render_template(
            "profile.html", username=username, dishes=dishes)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """ remove user from session cookies """
    session.clear()
    flash("You have been logged out")
    return redirect(url_for("login"))


@app.route("/search", methods=["GET", "POST"])
def search():
    """ Allows user to search for recipe on their profile page """
    query = request.form.get("query")
    dishes = list(mongo.db.dishes.find({"$text": {"$search": query}}))
    return render_template(
        "profile.html", username=session["user"], dishes=dishes)


@app.route("/recipe/<recipe_id>")
def individual_recipe(recipe_id):
    """ Gives details about individual recipe user has chosen """
    recipe = mongo.db.dishes.find_one({"_id": ObjectId(recipe_id)})
    return render_template(
        "individual_recipe.html", recipe=recipe)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    """ Allows user to add recipe to the website """
    if request.method == "POST":
        dish = {
            "region": request.form.get("region"),
            "dish_name": request.form.get("dish_name"),
            "ingredients": request.form.getlist("ingredients"),
            "recipe": request.form.getlist("recipe"),
            "equipment": request.form.getlist("equipment"),
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
    """ Allows user to edit a recipe they have uploaded """
    if request.method == "POST":
        dish = {
            "region": request.form.get("region"),
            "dish_name": request.form.get("dish_name"),
            "ingredients": request.form.get("ingredients").split(", "),
            "recipe": request.form.get("recipe").split(", "),
            "equipment": request.form.get("equipment").split(", "),
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
    """ Allows user to delete recipe they have uploaded """
    mongo.db.dishes.remove({"_id": ObjectId(recipe_id)})
    flash("Dish Successfully Removed")
    return redirect(url_for("profile", username=session["user"]))


@app.route("/manage_category")
def manage_category():
    """ Displays a list of the categories (regions) used by the website """
    categories = list(mongo.db.categories.find().sort("region", 1))
    return render_template("manage_category.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    """ Allows a new region to be created """
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
    """ Allows a region to be edited """
    if request.method == "POST":
        submit = {
            "region": request.form.get("region")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
        flash("Region Successfully Updated")
        return redirect(url_for('manage_category'))
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    """ Allows a region to be deleted """
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Region Successfully Deleted")
    return redirect(url_for("manage_category"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
