from flask import Flask
from flask_login import login_user
from flask import request, session
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb+srv://vercel-admin-user-641df86deec22841cd00f989:U7MK7TOONktRvOOR@cluster0.myy76mk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
app.config['MONGO_URI'] = 'mongodb+srv://vercel-admin-user-641df86deec22841cd00f989:U7MK7TOONktRvOOR@cluster0.myy76mk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
app.config['SECRET_KEY'] = 'a6d217d048fdcd227661b755'
db = client['Admin_BnB']
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "partbarse92@gmail.com"
app.config['MAIL_PASSWORD'] = "xdfrjwaxctwqpzyg"

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/home')
def home():
    return 'home page'

@app.route("/addUser", methods=["POST"])
def addUser():
    users = db['client_db']
    user = request.json
    print(user)
    name = user['usrnme']
    phone = user['phone']
    pwd = bcrypt.generate_password_hash(user['pwd']).decode('utf-8')
    email = user['email']
    uid = random.getrandbits(32)
    if users.find_one({"usrnme":name}) or users.find_one({"phone":phone}) or users.find_one({"email":email}):
        return {"isSuccess":"False", "msg":"Username or Phone number or Email already exist"}
    else:
        users.insert_one({
            'usrnme': name, 
            'pwd': pwd,
            'email': email,
            "phone":phone,
            "pic_url":"https://png.pngtree.com/png-clipart/20190924/original/pngtree-user-vector-avatar-png-image_4830521.jpg",
            "balance":"0",
            "uid":uid
            })
        return {"isSuccess":"True","msg":f"{name}'s data inserted", "details": {
            'usrnme': name, 
            'pwd': pwd,
            'email': email,
            "phone":phone,
            "pic_url":"https://png.pngtree.com/png-clipart/20190924/original/pngtree-user-vector-avatar-png-image_4830521.jpg",
            "balance":"0",
            "uid":uid
            }}

@app.route("/signIn", methods=["GET", "POST"])
def signIn():
    users = db["client_db"]
    if request.method == "GET":  # and "usrnme" not in session:
        # user = request.json
        # name = user["usrnme"]
        name = request.args.get("usrnme")
        password = request.args.get("pwd")
        # password = user["pwd"]
        logged_user = users.find_one({"usrnme": name})
        print(logged_user)
        if login_user:
            if logged_user:
                if bcrypt.check_password_hash(logged_user["pwd"], password):
                    session["usrnme"] = name
                    return {"isSuccess":"True", "details":{'usrnme': logged_user['usrnme'],'email': logged_user['email'],"phone":logged_user['phone'],"pic_url":"https://png.pngtree.com/png-clipart/20190924/original/pngtree-user-vector-avatar-png-image_4830521.jpg","balance":logged_user["balance"],"uid":logged_user["uid"]}}
                else:
                    return {"isSuccess":"False"}
            return {"isSuccess":"False"}
        return {"isSuccess":"False"}
    
@app.route("/logout")
def logout():
    name = request.args.get("usrnme")
    session.pop("usrnme", None)
    return f"{name.upper()} logged out successfully"

if __name__ == '__main__':
    app.run()