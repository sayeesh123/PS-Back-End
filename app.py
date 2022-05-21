from flask import Flask
from flask_cors import CORS
from psusers import users
from flask_mail import Mail
from dbconfig import conn 

app=Flask(__name__)
mail = Mail(app) 
app.config['SECRET_KEY'] = 'SP_Project_Secret_Key'

DB_Details = conn
 
CORS(app)

print(DB_Details)

app.register_blueprint(users)


if __name__ == '__main__':
    app.run()