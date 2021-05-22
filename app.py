from flask import Flask, render_template, jsonify, url_for, request, flash, current_app
from livereload import Server
from flaskext.mysql import MySQL
import pymysql.cursors
import json
import os
from colorama import init, Fore, Back, Style
from decouple import config

# initialize the flask app
app = Flask(__name__)

# flask app configuration
app.secret_key = config("SECRET_KEY")
app.config["MYSQL_DATABASE_HOST"] = config("DB_HOST", default="localhost")
app.config["MYSQL_DATABASE_DB"] = config("DB_NAME")
app.config["MYSQL_DATABASE_USER"] = config("DB_USER")
app.config["MYSQL_DATABASE_PORT"] = config("DB_PORT", cast=int)
app.config["MYSQL_DATABASE_PASSWORD"] = config("DB_PASSWORD")

# use a dictionary cursor object
mysql = MySQL(app, cursorclass = pymysql.cursors.DictCursor)

# Routes definition
@app.route("/", methods = ["GET", "POST"])
def index():
  return render_template("index.html")

@app.route("/admin/students/<id>")
def details(id):
  test = True
  # get students records
  try:
    connection = mysql.get_db()
    cursor = connection.cursor()
    cursor.execute("select * from students where id=%s", (id))
    cursor_output = cursor.fetchall()
    if len(cursor_output) <= 0:
      raise Exception
    connection.close()
    response = {"student": cursor_output[0]}
    response["student"]["gender"] = "Male" if response["student"]["gender"] == "M" else "Female"
  except Exception:
    test = False
    print(f"Error: could not get details of student with id={id}")
  if test:
    return render_template("details.html", response = response)
  else:
    return render_template("error.html", response = response)

@app.route("/students/portal/")
def portal():
  return render_template("portal.html")

# @app.route("/admin/dashboard/")
# def students():
#   # get students records
#   connection = mysql.get_db()
#   cursor = connection.cursor()
#   cursor.execute("select * from students")
#   cursor_output = cursor.fetchall()
#   connection.close()
#   response = {"students": cursor_output}
#   return render_template("students.html", response = response)

@app.route("/admin/dashboard/")
def students():
  # get the query parameters
  try:
    name = request.args.get("name")
    status = request.args.get("status")
    gender = request.args.get("gender")
    jamb = request.args.get("jamb")
  except Exception:
    print(f"Some values were not supplied in the query!")
  finally:
    if gender is not None:
      if gender.lower() == "male":
        gender = "M"
    elif gender is not None:
      if gender.lower() == "female":
        gender = "F"
    else:
      gender = ""
    # check if any value was not provided
    if name is None:
      name = ""
    if status is None:
      status = ""
    if gender is None:
      gender = ""
    if jamb is None:
      jamb = ""
    # concatenate the column values with wildcards for search
    name = "%" + name + "%"
    status = "%" + status + "%"
    gender = "%" + gender + "%"

  # get students records
  connection = mysql.get_db()
  cursor = connection.cursor()
  cursor.execute("select * from students where (firstname like %s  or lastname like %s or middlename like %s) and status like %s and gender like %s and jamb >= %s", (name, name, name, status, gender, jamb))
  cursor_output = cursor.fetchall()
  connection.close()
  response = {"students": cursor_output}
  return render_template("students.html", response = response)

@app.route("/api/get-states-lga/")
def get_states_lga():
  try:
    with open("assets/states-localgovts.json") as f:
      data = json.load(f)
  except:
    print(f"{Back.RED}Could not read json data!{Style.RESET_ALL}")
  return jsonify(data)

@app.route("/api/register", methods = ["POST"])
def register():
  print(f"{Style.RESET_ALL}")
  test = True
  try:
    # get image data
    image = request.files["image"]
    filename = image.filename
    filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
    print(filepath)
    image.save(filepath)
    #get form data
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    middlename = request.form["middlename"]
    email = request.form["email"]
    dob = request.form["dob"]
    gender = request.form["gender"]
    phonenumber = request.form["phonenumber"]
    address = request.form["address"]
    state = request.form["state"]
    lga = request.form["lga"]
    kin = request.form["kin"]
    jamb = request.form["jamb"]
    # validate form data
    if(filename.strip() == "" or firstname.strip() == "" or lastname.strip() == "" or email.strip() == "" or dob.strip() == "" or gender.strip() == "" or phonenumber.strip() == "" or address.strip() == "" or state.strip() == "" or lga.strip() == "" or kin.strip() == "" or jamb.strip() == ""):
      test = False
    else:
      if(not jamb.isnumeric()):
        test = False
    if test:
      try:
        connection = mysql.get_db()
        cursor = connection.cursor()
        cursor.execute("insert into students (image, firstname, lastname, middlename, email, dob, gender, phonenumber, address, state, lga, kin, jamb) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (filename, firstname, lastname, middlename, email, dob, gender, phonenumber, address, state, lga, kin, jamb))
        connection.commit()
        connection.close()
      except Exception:
        test = False
        message = f"Error did not submit students information!"
        print(f"{Back.RED}Insertion error: Was not able to insert to table!{Style.RESET_ALL}")
  except Exception:
    test = False
    message = f"Error one or more inputs filled incorrectly!"
    print(f"{Back.RED}Error while processing the request!{Style.RESET_ALL}")
  finally:
    if test:
      return jsonify({
        "status": "success",
        "message": "Successfully registered user!"
      })
    else:
      return jsonify({
        "status": "fail",
        "message": message
      })

@app.route("/api/status/<id>", methods = ["POST"])
def change_status(id):
  print(f"{Style.RESET_ALL}")
  test = True
  try:
    status = request.json["status"]
    # validate form data
    if(status.strip() == ""):
      test = False
    if test:
      try:
        connection = mysql.get_db()
        cursor = connection.cursor()
        cursor.execute("update students set status=%s where id=%s", (status, id))
        connection.commit()
        connection.close()
      except Exception:
        test = False
        print(f"{Back.RED}Update error: Was not able to update to table!{Style.RESET_ALL}")
  except Exception:
    test = False
    print(f"{Back.RED}Error while processing the request!{Style.RESET_ALL}")
  finally:
    if test:
      return jsonify({"status": "success"})
    else:
      message = f"Error did not update table!"
      return jsonify({
        "status": "fail",
        "message": message
        })

if __name__ == "__main__":
  init()
  mode = config("DEBUB", default=True, cast=bool)
  try:
    if mode:
      app.run()
    else:
      init() # initialize colorama
      # app.run(debug = True, port = 5500)
      app.debug = True
      server = Server(app.wsgi_app)
      server.serve()
  except Exception:
    print(f"{Back.RED}Could not determine if in production of development machine!")