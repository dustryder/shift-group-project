# BCIT105Z - Project 1 - Grupo 1
# Amanda Macauley, incitatus26@hotmail.com
# Jess Forbes, jessieforbes.nz@gmail.com
# Feng Zhou, jfzhou05@gmail.com
# Rodrigo Marcolino, rodrigomarcolino@gmail.com
# 29/04/2020

from flask import Flask, render_template, request, session, redirect
import mysql.connector
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
    device_name = db.Column(db.String(30))
    device_type = db.Column(db.String(30))
    os_type = db.Column(db.String(10))
    os_version = db.Column(db.String(10))
    ram = db.Column(db.String(10))
    device_cpu = db.Column(db.String(50))
    device_bit = db.Column(db.CHAR(2))
    resolution = db.Column(db.String(30))
    grade = db.Column(db.String(10))
    uuid = db.Column(db.String(50))
    acquisition_date = db.Column(db.Date)


class Employee(db.Model):
    __tablename__ = 'employee'

    employee_id = db.Column(db.INTEGER, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    location = db.Column(db.String(30))
    permissions = db.Column(db.INTEGER)

class UserView(ModelView):

    create_modal = True
    edit_modal = True

admin.add_view(UserView(Device, db.session))
admin.add_view(UserView(Employee, db.session))

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
<<<<<<< HEAD
        
        #add device location to homepage table, # add DeviceVault as default location for unassigned devices 
        mycursor.execute("SELECT device.device_id, device_name, first_name, device_type,os_type, os_version, grade, IFNULL(Location, 'DeviceVault') AS Location FROM Device LEFT JOIN deviceloan on device.device_id = deviceloan.device_id LEFT JOIN employee on employee.employee_id = deviceloan.employee_id")
=======
        #mycursor.execute("SELECT device_id, device_name, first_name, device_type, os_type, os_version, grade FROM devicestatus ORDER BY device_id")
        #add device location to homepage table
        mycursor.execute("SELECT device.device_id, employee.employee_id, device_name, first_name, device_type, os_type, os_version, grade, location FROM device LEFT JOIN deviceloan on device.device_id = deviceloan.device_id LEFT JOIN employee on employee.employee_id = deviceloan.employee_id")
>>>>>>> 9473503104dce843ae3a456b0a13b81503982c0c
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
        device_id, available = device_id.split(',')
        employee_id = request.form['employee_id']
        employee_id, employee_name, _ = employee_id.split(',')
        #Store the employee id of the person trying to borrow or return a device
        session['employee_id'] = employee_id

        if available != "available":
            query = f"DELETE FROM deviceloan WHERE device_id = {device_id}"
            mycursor.execute(query)
        else:
            query = f"INSERT INTO deviceloan (device_id, employee_id) VALUE ({device_id},{employee_id})"
            mycursor.execute(query)
        connection.commit()

        #We are retrieving the devices/employees again to update the homepage with the changes we've made
        mycursor.execute("SELECT device.device_id, employee.employee_id, device_name, first_name, device_type, os_type, os_version, grade, location FROM device LEFT JOIN deviceloan on device.device_id = deviceloan.device_id LEFT JOIN employee on employee.employee_id = deviceloan.employee_id")
        device_table = mycursor.fetchall()

        mycursor.execute("SELECT employee_id, first_name, permissions FROM employee")
        employees = mycursor.fetchall()

        #add device location, DeviceVault as default location for unassigned devices 
        mycursor.execute("SELECT device.device_id, device_name, first_name, device_type,os_type, os_version, grade, IFNULL(Location, 'DeviceVault') AS Location FROM Device LEFT JOIN deviceloan on device.device_id = deviceloan.device_id LEFT JOIN employee on employee.employee_id = deviceloan.employee_id")
        device_table = mycursor.fetchall()

        query = f"SELECT permissions FROM employee WHERE employee_id = '{employee_id}'"
        mycursor.execute(query)
        permission = mycursor.fetchone()[0]
        

    return render_template('hometable.html',device_table=device_table, employees=employees, permission=permission, employee_id=employee_id)
        
if (__name__) == ('__main__'):
    app.run(debug=True)