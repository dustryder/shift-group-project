# BCIT105Z - Project 1 - Grupo 1
# Amanda Macauley, incitatus26@hotmail.com
# Jess Forbes, jessieforbes.nz@gmail.com
# Feng Zhou, jfzhou05@gmail.com
# Rodrigo Marcolino, rodrigomarcolino@gmail.com
# 29/04/2020

from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error, errorcode
from config_db import config

from flask import Flask
app = Flask(__name__)


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


#Function to render basi device table on homepage of web application
@app.route("/", methods = ['POST', 'GET'])
def home():

    try:
        connection = get_db_connection()
        mycursor = connection.cursor()
        mycursor.execute("SELECT device_id, device_name, status, device_type, os_type, os_version, grade FROM Device")
        device_table = mycursor.fetchall()

        mycursor.execute("SELECT employee_id, first_name FROM employee")
        employees = mycursor.fetchall()

    except mysql.connector.Error as error:
        print("Error reading Device table {}".format(error))  

    if request.method == 'POST':

        device_id = request.form['device_id']
        device_id, available = device_id.split(',')
        employee_id = request.form['employee_id']
        employee_id, employee_name = employee_id.split(',')

        if available != "available":
            mycursor.execute(f"UPDATE device SET status = 'available' WHERE device_id = {device_id}")
        else:
            mycursor.execute(f"UPDATE device SET status = '{employee_name}' WHERE device_id = {device_id}")
        connection.commit()

        #We are retrieving the devices/employees again to update the homepage with the changes we've made
        mycursor.execute("SELECT device_id, device_name, status, device_type, os_type, os_version, grade FROM Device")
        device_table = mycursor.fetchall()

        mycursor.execute("SELECT employee_id, first_name FROM employee")
        employees = mycursor.fetchall()

    return render_template('hometable.html',device_table=device_table, employees=employees)
        
if (__name__) == ('__main__'):
    app.run(debug=True)