from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from bson import ObjectId
import os

load_dotenv()

app = Flask(__name__)


app.config["MONGO_URI"] = os.getenv("MONGO_URI")

app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

mysql = MySQL(app)
mongo = PyMongo(app)

@app.route("/add_mongo", methods=["POST"])
def add_mongo():

    nombre = request.json["nombre"]
    edad = request.json["edad"]
    genero = request.json["genero"]
    color = request.json["color"]

    if nombre and edad and genero and color:

        id = mongo.db.insert_one({

            "nombre":nombre,
            "edad":edad,
            "genero":genero,
            "color":color
        })

        response = {
            "id":id,
            "nombre":nombre,
            "edad":edad,
            "genero":genero,
            "color":color
        }

        return jsonify(response)

@app.route('/get_mongo')
def get_mongo():
    
    gatos = mongo.db.gatos.find()

    return jsonify(gatos)



@app.route('/add_sql')
def add_sql():
    nombre = request.json["nombre"]
    edad = request.json["edad"]
    genero = request.json["genero"]
    color = request.json["color"]

    if nombre and edad and genero and color:

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO gatos VALUES(NULL,%s,%s,%s,%s)",(nombre,edad,genero,color))
        

        return jsonify({"message":"Datos insertados correctamente"})

@app.route('/get_sql',methods=["GET"])
def get_sql():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM gatos")
    sql = cursor.fetchall()

    return jsonify(sql)


@app.route('/get_sql/<id>',methods=["GET"])
def get_sqlid(id):
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM gatos WHERE id=%s", (id,))
    sql = cursor.fetchall()

    return jsonify(sql)



@app.route('/delete_sql/<id>',methods=["DELETE"])
def delete_sql(id):
    
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE id FROM gatos WHERE id=%s", (id,))
    mysql.commit()
    return jsonify({"message":"eliminado con éxito"})


@app.route('/update_sql', methods=["PUT"])
def update_sql():

    nombre = request.json["nombre"]
    edad = request.json["edad"]
    genero = request.json["genero"]
    color = request.json["color"]

    if nombre and edad and genero and color:

        cursor = mysql.connection.cursor()

        cursor.execute("UPDATE from gatos $SET nombre=%s,edad=%s,genero=%s,color=%s WHERE id=%s", (nombre,edad,genero,color))

        return jsonify({"message":"Se ha actualizado correctamente"})


if __name__ == "__main__":
    app.run(debug=True)
    