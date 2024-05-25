from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "worlddata"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>HAYS</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/countries", methods=["GET"])
def get_countries():
    data = data_fetch("""SELECT * FROM worlddata.countries""")
    return make_response(jsonify(data), 200)


@app.route("/countries/<int:id>", methods=["GET"])
def get_countries_by_id(id):
    data = data_fetch(
        """SELECT * FROM worlddata.countries WHERE CountryID = {}""".format(id)
    )
    return make_response(jsonify(data), 200)


@app.route("/Continents", methods=["GET"])
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
    print("row(s) affected:", rows_affected)
    cur.close()
    return make_response(
        jsonify(
            {"message": "country added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/countries/<int:id>", methods=["PUT"])
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
