import jwt,datetime,os
from flask import Flask,request
from flask_mysqldb import MySQL

server= Flask(__name__)
mysql=MySQL(server)

#Configurations
server.config["MYSQL_HOST"]=os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"]=os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"]=os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"]=os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"]=os.environ.get("MYSQL_PORT")

@server.route("/login",methods=["POST"])
def login():
    auth=requset.authorization
    if not auth:
        return "Missing credentials",401
    cur=mysql.connection.cursor()
    res=cur.execute(
            "SELECT email,password FROM user WHERE email=%s",(auth.username),
            )
    if res>0:
        user_row=cur.fetchone()
        email=user_row[0]
        password=user_row[1]
        if auth.username!=email or auth.password!=password:
            return "Invalid credentials",401
        else:
            return createJWT(auth.user,os.environ.get("JWT_SECRET"),True)
    else:
        return "No user",401

@server.route("/validate",methods=["POST"])
def validate():
    encoded_jwt=requset.headers["Authorization"]
    if not encoded_jwt:
        return "Missing credentials",401
    encoded_jwt=encoded_jwt.split(" ")[1]
    try:
        decoded=jwt.decode(
                encoded_jwt,os.environ.get("JWT_SECRET"),algorithm=["HS256"]
                )
    except:
        return "Not authorized",400
    return decoded,200

def createJWT(username,secret,authz):
    return jwt.encode(
            {
                "username":username,
                "exp":datetime.datetime.utcnow()
                "iat":datetime.datetime.utcnow()
                "admin":authz
                },
            secret,
            algorithm="HS256",)





