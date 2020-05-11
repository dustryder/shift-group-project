#from app import app

PASSWORD = '12345'

config = {
  "user":"root",
  "password":f"{PASSWORD}",
  "host":"127.0.0.1",
  "database":"Devices",
  "auth_plugin":"mysql_native_password",
  "raise_on_warnings":True,
  "autocommit": True  
}

SECRET_KEY = 'G04ps8f_7Wm3kRyDc480Dg8884'
DATABASE_URI = f'mysql+mysqlconnector://root:{PASSWORD}@localhost/devices'
