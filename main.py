from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap5
import requests
from database import tasks
from bson.objectid import ObjectId


app = Flask(__name__)
bootstrap = Bootstrap5(app)

user = "User"
city = "Katowice"
is_admin = False
users = ["Zyzio", "Dyzio", "Krzysztof"]
country = {
    "name":"Polska",
    "capital":"Warszawa"
}


@app.route("/")
def hello_world():
    return render_template("index.html",
                           user=user,
                           users=users,
                           city=city,
                           is_admin=is_admin,
                           country=country
                           )


@app.route("/o-nas")
def about_page():
    return "<h1>Informacje o nas...</h1>" 


@app.route("/kraje")
def countries_page():
    response = requests.get("https://restcountries.com/v3.1/all")
    if response.ok:
        countries = response.json()
        return render_template("countries2.html", countries=countries)
    else:
        return f"Błąd {response.status_code}"


@app.route("/kraje/<code>")
def details_page(code):
    response = requests.get(f"https://restcountries.com/v3.1/alpha/{code}")
    if response.ok:
        country = response.json()

        border_countries = ""
        if country[0].__contains__("borders"):
            borders= ",".join(country[0]["borders"])
            response2 = requests.get(f"https://restcountries.com/v3.1/alpha?codes={borders}")
            border_countries = response2.json()

        return render_template("details.html", 
                               country=country[0],
                               borders=border_countries
                               )
    else:
        return f"Błąd {response.status_code}"
    
    
@app.route("/results", methods=["GET","POST"])
def search_result_page():
    query = request.form["query"]
    response = requests.get(f"https://restcountries.com/v3.1/name/{query}")
    countries = response.json()

    return render_template("result.html",countries=countries)
    # if response.ok:
    #     countries = response.json()
    #     return render_template("countries2.html", countries=countries)
    # else:
    #     return f"Błąd {response.status_code}"


@app.route("/zadania")
def all_tasks():
    tasks_list = tasks.find({})
    return render_template("tasks.html", tasks_list = tasks_list)


@app.route("/dodaj-zadanie",methods=["GET","POST"])
def create_task():
    new_task = {
        "title": request.form["tytul"],
        "category": request.form["kategoria"]
    }
    tasks.insert_one(new_task)
    return redirect("/zadania", code=302)


@app.route("/usun-zadanie", methods=["GET", "POST"])
def delete_task():
    id = request.form["id"]
    tasks.delete_one({"_id": ObjectId(id)})
    return redirect("/zadania", code=302)


@app.errorhandler(404)
def not_found(e):
    return "Błąd. Nie znaleziono strony."