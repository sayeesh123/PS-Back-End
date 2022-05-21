from flask import Blueprint
from flask import Flask, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS  
import psycopg2.extras
import re
from flask_mail import Mail, Message
from dbconfig import SQL , conn

print(SQL)
users = Blueprint('users', __name__)
CORS(users)


# validations for EMAIL , PASSWORD , PHONE NUMBER
email_valid = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
password_valid = re.compile('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
phone_valid = re.compile("^[0-9]{10}$")

# Register user
@users.route('/ps_register', methods=['POST', 'GET'])
def register():
    _json = request.json
    _emailid = _json['email_id']
    _username = _json['username']
    _password = _json['password']
    _phone = _json['phone_number']

    if request.method == 'POST':
        if _username and _password and _emailid  and _phone:
            if(re.search(email_valid, _emailid)):
                if re.search(phone_valid, _phone):
                    if(re.search(password_valid, _password)):       
                        passhash = generate_password_hash(_password)
                        SQL.execute(
                            "SELECT * FROM sp_users WHERE email_id ='{0}'".format(_emailid))
                        # For user already exist
                        if SQL.fetchone() is not None:
                            resp = jsonify(
                                {'message': 'Entered email id already exist , Please login', 'alreadyexist': True, "status": False})
                            resp.status_code = 200
                            return resp
                        # print("INSERT INTO users (username , password , email_id)  VALUES ('{0}' ,'{1}' ,'{2}'))".format(_username,passhash,_emailid))
                        sql = "INSERT INTO sp_users (username , password , email_id,phone_number)  VALUES ('{0}' ,'{1}' ,'{2}','{3}')".format(
                            _username, passhash, _emailid, _phone)
                        print(sql)
                        SQL.execute(sql)
                        conn.commit()
                        SQL.close()
                        resp = jsonify(
                            {'message': 'Account created Successfully', "status": True})
                        resp.status_code = 200
                        return resp
                    # Checking the valid password with uppercase , lowercase , special character , length 6
                    else:
                        resp = jsonify(
                            {'message': 'Password should must be length 6 , with uppercase , lowercase , digit and special character', 'status': False})
                        resp.status_code = 200
                        return resp

                else:
                    resp = jsonify(
                        {'message': "Please enter valid phone number with 10 digits", 'status': False})
                    resp.status_code = 200
                    return resp

            # For checking the invalid email
            else:
                resp = jsonify(
                    {'message': 'Please enter valid email id', 'status': False})
                resp.status_code = 200
                return resp

        # For empty values of email , password , username
        elif _username == '' or _password == '' or _emailid == '' or _phone=='':
            resp = jsonify(
                {'message': 'Please enter missed keys', 'status': False})
            resp.status_code = 200
            return resp
    elif request.method == 'GET':
        resp = jsonify(
            {'message': 'Bad Request! , Please check your request method', 'status': False})
        resp.status_code = 400
        return resp

