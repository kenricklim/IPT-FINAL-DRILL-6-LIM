from flask import Flask, request, jsonify, make_response, render_template
from flask_mysqldb import MySQL
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)


app.config["SECRET_KEY"] = "VCJ7E1E57OwtFPHMx5E"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "worlddata"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"Alert!": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = data["user"]
        except:
            return jsonify({"Message": "Invalid token"}), 403

        return func(*args, **kwargs)

    return decorated


@app.route("/")
def hello_world():
    return "<p>WELCOME TO MY FLASK APPLICATION!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/public")
def public():
    return "For Public"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")

        if username == "admin" and password == "123456":
            token = jwt.encode(
                {"user": username, "exp": datetime.utcnow() + timedelta(minutes=30)},
                app.config["SECRET_KEY"],
                algorithm="HS256",
            )

            return jsonify({"token": token.decode("utf-8")})
        else:
            return make_response(
                "Unable to verify",
                403,
                {"WWW-Authenticate": 'Basic realm: "Authentication Failed "'},
            )
    else:
        return render_template("login.html")


@app.route("/countries", methods=["GET"])
def get_countries():
    data = data_fetch("""SELECT * FROM worlddata.countries""")
    return make_response(jsonify(data), 200)


@app.route("/countries/<int:id>", methods=["GET"])
@token_required
def get_countries_by_id(id):
    data = data_fetch(
        """SELECT * FROM worlddata.countries WHERE CountryID = {}""".format(id)
    )
    return make_response(jsonify(data), 200)


@app.route("/Continents", methods=["GET"])
@token_required
def get_continents_with_more_than_five_countries():
    query = """
    SELECT Continent, COUNT(CountryID) AS CountryCount, SUM(Population) AS TotalPopulation
    FROM WorldData.Countries
    GROUP BY Continent
    HAVING COUNT(CountryID) > 5;
    """
    data = data_fetch(query)

    response = {
        "Continents": data,
        "CountryCount": len(data),
        "TotalPopulation": sum(item["TotalPopulation"] for item in data),
    }

    return make_response(jsonify(response), 200)


@app.route("/countries", methods=["POST"])
@token_required
def add_country():
    cur = mysql.connection.cursor()
    info = request.get_json()
    CountryName = info["CountryName"]
    Continent = info["Continent"]
    Population = info["Population"]
    cur.execute(
        """INSERT INTO worlddata.countries (CountryName, Continent, Population) VALUES (%s, %s, %s)""",
        (CountryName, Continent, Population),
    )

    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "country added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/countries/<int:id>", methods=["PUT"])
@token_required
def update_country(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    CountryName = info["CountryName"]
    Continent = info["Continent"]
    Population = info["Population"]
    cur.execute(
        """
        UPDATE worlddata.countries SET CountryName = %s, Continent = %s, Population = %s WHERE CountryID = %s
        """,
        (CountryName, Continent, Population, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "country updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/countries/<int:id>", methods=["DELETE"])
@token_required
def delete_country(id):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM worlddata.countries WHERE CountryID = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "country deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
