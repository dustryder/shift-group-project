#from app import app

PASSWORD = 'Gryphon11'

config = {
  "user":"shift2020",
  "password":f"{PASSWORD}",
  "host":"shift2020.mysql.pythonanywhere-services.com",
  "database":"shift2020$devices",
  "auth_plugin":"mysql_native_password",
  "raise_on_warnings":True,
  "autocommit": True
}

SECRET_KEY = 'G04ps8f_7Wm3kRyDc480Dg8884'
DATABASE_URI = f'mysql+mysqlconnector://shift2020:{PASSWORD}@shift2020.mysql.pythonanywhere-services.com/shift2020$devices'