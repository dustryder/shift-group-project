# BCIT105Z - Project 1 - Grupo 1
# Amanda Macauley, incitatus26@hotmail.com
# Jess Forbes, jessieforbes.nz@gmail.com
# Feng Zhou, jfzhou05@gmail.com
# Rodrigo Marcolino, rodrigomarcolino@gmail.com
# 29/04/2020

from flask import Flask, render_template, request, session, redirect, jsonify
import mysql.connector
import datetime
from mysql.connector import Error, errorcode
from config_db import config, DATABASE_URI, SECRET_KEY
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

from flask import Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
admin = Admin(app, base_template='layout.html', template_mode='bootstrap3')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

db = SQLAlchemy(app)

class Device(db.Model):
    __tablename__ = 'device'

    device_id = db.Column(db.INTEGER, primary_key=True)
    device_name = db.Column(db.String(30), unique=True)
    device_type = db.Column(db.String(30))
    os_type = db.Column(db.Enum('Windows', 'Android', 'IOS', 'VR'))
    os_version = db.Column(db.String(10))
    ram = db.Column(db.String(10))
    device_cpu = db.Column(db.String(50))
    device_bit = db.Column(db.Enum('32', '64'))
    resolution = db.Column(db.String(30))
    grade = db.Column(db.Enum('Obsolete', 'Low', 'Medium', 'Low - Mid', 'High', 'Mid - High'))
    uuid = db.Column(db.String(50))
    acquisition_date = db.Column(db.Date)


class Employee(db.Model):
    __tablename__ = 'employee'

    employee_id = db.Column(db.INTEGER, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    location = db.Column(db.Enum('Office 1', 'Office 2'))
    permissions = db.Column(db.INTEGER)

admin.add_view(ModelView(Device, db.session))
admin.add_view(ModelView(Employee, db.session))

#secret key needed for securely signing the session cookie.

#Function for get Database connection
def get_db_connection():
    """Get Database connection"""
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as error :
        print("Failed to connect to database {}".format(error))

#Function  for Close Database connection        
def close_db_connection(connection):
    """Close Database connection"""
    try:
        connection.close()
    except mysql.connector.Error as error :
        print("Failed to close database connection {}".format(error))

#session functions to remember user; still needs work
@app.before_request
def make_session_permanent():
   session.permanent = True 

@app.route("/loan-device", methods = ['POST'])
def loan():

    connection = get_db_connection()
    mycursor = connection.cursor()

    device_id = request.form['device_id']
    employee_id = request.form['employee_id']
    loan_end = request.form['loan_end']

    query = f"INSERT INTO deviceloan (device_id, employee_id, loan_start, loan_end) VALUE ({device_id}, {employee_id}, CURDATE(), '{loan_end}')"
    mycursor.execute(query)
    connection.commit()

    return redirect("/")

@app.route("/device-history", methods = ['GET', 'POST'])
def history():

    connection = get_db_connection()
    mycursor = connection.cursor()

    if request.method == 'POST':
        device = request.get_json(force=True)
        device_id = device['device_id']

        query = f"SELECT * FROM devicehistory WHERE device_id = %s ORDER BY returned_date DESC"
        mycursor.execute(query,(device_id,))

        history = mycursor.fetchall()
        history = [attribute[1:] for attribute in history]

        query = f"SELECT * FROM deviceinfo WHERE device_id = %s"
        mycursor.execute(query, (device_id,))

        info = mycursor.fetchall()
        info = [attribute[1:] for attribute in info]

    return jsonify([history, info]);

@app.route("/login", methods = ['POST'])
def login():

    employee = request.get_json(force=True)
    session['employee_id'] = int(employee['employee_id'])
    return redirect("/")

#Function to render basic device table on homepage of web application
@app.route("/", methods = ['POST', 'GET'])
def home():

    try:
        connection = get_db_connection()
        mycursor = connection.cursor()
        
        #add device location to homepage table, # add DeviceVault as default location for unassigned devices 
        query = "SELECT * FROM devicetable "
        mycursor.execute(query)
        device_table = mycursor.fetchall()

        mycursor.execute("SELECT employee_id, first_name, permissions FROM employee")
        employees = mycursor.fetchall()


    except mysql.connector.Error as error:
        print("Error reading Device table {}".format(error))  

    #Try to retrieve stored employee_id from session. If one has not been stored, return the employee id of a known plebeian
    employee_id = session.get('employee_id', 1)
    #Retrieve the permissions level of the employee_id we just received
    query = f"SELECT permissions FROM employee WHERE employee_id = {employee_id}"
    mycursor.execute(query)
    #Set permissions, ready to be sent to the template
    permission = mycursor.fetchone()[0]

    if request.method == 'POST':

        device_id = request.form['device_id']
        device_id, available, loan_start = device_id.split(',')
        employee_id = request.form['employee_id']
        employee_id, employee_name, _ = employee_id.split(',')
        #Store the employee id of the person trying to borrow or return a device
        session['employee_id'] = employee_id

        if available != "available":
            query = f"UPDATE deviceloan SET returned_date = CURDATE() WHERE device_id = {device_id} AND loan_start = '{loan_start}'"
            mycursor.execute(query)
        else:
            query = f"INSERT INTO deviceloan (device_id, employee_id) VALUE ({device_id},{employee_id})"
            mycursor.execute(query)
        connection.commit()

        mycursor.execute("SELECT employee_id, first_name, permissions FROM employee")
        employees = mycursor.fetchall()

        #add device location, DeviceVault as default location for unassigned devices 
        query = "SELECT * FROM devicetable"
        mycursor.execute(query)
        device_table = mycursor.fetchall()

        query = f"SELECT permissions FROM employee WHERE employee_id = '{employee_id}'"
        mycursor.execute(query)
        permission = mycursor.fetchone()[0]


    query = "SELECT device_id FROM deviceloan WHERE returned_date IS NULL AND loan_end < NOW()"
    mycursor.execute(query)
    overdue_devices = [x[0] for x in mycursor.fetchall()]

    #add filter and flag for new devices
    query = "SELECT device_id FROM device WHERE acquisition_date BETWEEN DATE_ADD(CURDATE(), INTERVAL -7 DAY) AND CURDATE() ORDER BY acquisition_date DESC"
    mycursor.execute(query)
    new_devices = [x[0] for x in mycursor.fetchall()]
        
    return render_template('hometable.html',device_table=device_table, employees=employees, permission=permission, employee_id=employee_id, overdue_devices=overdue_devices, new_devices=new_devices)
        

if (__name__) == ('__main__'):
    app.run(debug=True)