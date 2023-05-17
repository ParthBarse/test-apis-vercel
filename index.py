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
import json

app = Flask(__name__)
CORS(app)

client = MongoClient(
    'mongodb+srv://vercel-admin-user-641df86deec22841cd00f989:U7MK7TOONktRvOOR@cluster0.myy76mk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
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
    if users.find_one({"usrnme": name}) or users.find_one({"phone": phone}) or users.find_one({"email": email}):
        return {"isSuccess": "False", "msg": "Username or Phone number or Email already exist"}
    else:
        users.insert_one({
            'usrnme': name,
            'pwd': pwd,
            'email': email,
            "phone": phone,
            "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
            "balance": "0",
            "uid": uid
        })
        return {"isSuccess": "True", "msg": f"{name}'s data inserted", "details": {
            'usrnme': name,
            'pwd': pwd,
            'email': email,
            "phone": phone,
            "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
            "balance": 0,
            "uid": uid
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
                    return {"isSuccess": "True", "details": {'usrnme': logged_user['usrnme'], 'email': logged_user['email'], "phone": logged_user['phone'], "pic_url": logged_user['pic_url'], "balance": logged_user["balance"], "uid": logged_user["uid"]}}
                else:
                    return {"isSuccess": "False"}
            return {"isSuccess": "False"}
        return {"isSuccess": "False"}


@app.route("/addbalance", methods=["GET"])
def addbalance():
    users = db["client_db"]
    if request.method == "GET":  # and "usrnme" not in session:
        # user = request.json
        # name = user["usrnme"]
        name = request.args.get("usrnme")
        uid = request.args.get("uid")
        uid = int(uid)
        addMoney = request.args.get("addMoney")
        # password = user["pwd"]
        logged_user = users.find_one({"usrnme": name})
        print(logged_user)
        if logged_user:
            prev_bal = logged_user["balance"]
            if (int(prev_bal)+int(addMoney)) <= 10000:
                new_bal = int(prev_bal)+int(addMoney)
                new_data = {"$set": {
                    "balance": new_bal
                }}
                users.update_one({"uid": uid}, new_data)
                return {"isSuccess": "True", "details": {"balance": new_bal, "uid": logged_user["uid"]}}
            else:
                return {"isSuccess": "False", "msg": "Cannot add more than Rs 10,000"}
        else:
            return {"isSuccess": "False", "msg": "Invalid Data"}


@app.route("/bookticket", methods=["GET"])
def bookticket():
    users = db["client_db"]
    tickets = db["clients_tickets"]
    if request.method == "GET":  # and "usrnme" not in session:
        # user = request.json
        # name = user["usrnme"]
        price = request.args.get("price")
        price = int(price)
        uid = request.args.get("uid")
        uid = int(uid)
        to_place = request.args.get("to_place")
        from_place = request.args.get("from_place")
        # password = user["pwd"]
        logged_user = users.find_one({"uid": uid})
        print(logged_user)
        if logged_user:
            prev_bal = logged_user["balance"]
            if (int(prev_bal)-int(price)) <= prev_bal:
                new_bal = int(prev_bal)-int(price)
                new_data = {"$set": {
                    "balance": new_bal
                }}
                users.update_one({"uid": uid}, new_data)

                import time
                curr_time = time.strftime("%H:%M:%S", time.localtime())

                if tickets.find_one({"uid": uid}):
                    f_data = tickets.find_one({"uid": uid})
                    all_tickets = f_data["tickets"]
                    data = {
                        "date": "12-5-2023",
                        "time": curr_time,
                        "from": from_place,
                        "to": to_place,
                        "price": price,
                    }
                    all_tickets.append(data)
                    new_data = {"$set": {
                        "tickets": all_tickets
                    }}
                    tickets.update_one({"uid": uid}, new_data)

                else:
                    data = {
                        "uid": uid,
                        "tickets": [{
                            "date": "12-5-2023",
                            "time": curr_time,
                            "from": from_place,
                            "to": to_place,
                            "price": price,
                        }]
                    }
                    tickets.insert_one(data)
                return {"isSuccess": "True", "details": {"balance": new_bal, "uid": logged_user["uid"]}}
            else:
                return {"isSuccess": "False", "msg": "Cannot add more than Rs 10,000"}
        else:
            return {"isSuccess": "False", "msg": "Invalid Data"}

# ------------------------------------------------------------------------------------------------------------

@app.route("/addAdmin", methods=["POST"])
def addAdmin():
    users = db['admin_db']
    user = request.json
    print(user)
    name = user['usrnme']
    phone = user['phone']
    pwd = bcrypt.generate_password_hash(user['pwd']).decode('utf-8')
    email = user['email']
    if users.find_one({"usrnme": name}) or users.find_one({"phone": phone}) or users.find_one({"email": email}):
        return {"isSuccess": "False", "msg": "Username or Phone number or Email already exist"}
    else:
        users.insert_one({
            'usrnme': name,
            'pwd': pwd,
            'email': email,
            "phone": phone,
            "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
            "total_earning": 0,
            "total_customers":0,
            "total_products":0
        })
        return {"isSuccess": "True", "msg": f"{name}'s data inserted", "details": {
            'usrnme': name,
            'pwd': pwd,
            'email': email,
            "phone": phone,
            "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4="
        }}

@app.route("/signInAdmin", methods=["GET", "POST"])
def signInAdmin():
    users = db["admin_db"]
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
                    return {"isSuccess": "True", "details": {'usrnme': logged_user['usrnme'], 'email': logged_user['email'], "phone": logged_user['phone'], "pic_url": logged_user['pic_url'], "total_earning": logged_user['total_earning'], "total_customers": logged_user['total_customers'], "total_products": logged_user['total_products']}}
                else:
                    return {"isSuccess": "False"}
            return {"isSuccess": "False"}
        return {"isSuccess": "False"}
    
    
@app.route("/signInClient", methods=["GET", "POST"])
def signInClient():
    users = db["client_db_esp"]
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
                    return {"isSuccess": "True", "details": {'usrnme': logged_user['usrnme'], 'email': logged_user['email'], "phone": logged_user['phone'], "pic_url": logged_user['pic_url'], "balance": logged_user['balance'], "rfid": logged_user['rfid']}}
                else:
                    return {"isSuccess": "False"}
            return {"isSuccess": "False"}
        return {"isSuccess": "False"}


@app.route("/readRFID", methods=["GET"])
def readRFID():
    users = db["client_db_esp"]
    amount_db = db['current_payment']
    if request.method == "GET":  # and "usrnme" not in session:
        rfid = request.args.get("rfid")
        if users.find_one({"rfid": rfid}):
            user_account = users.find_one({"rfid": rfid})
            user_balance = user_account["balance"]
            user_balance = int(user_balance)
            amount_to_deduct_obj = amount_db.find_one({"current": "1"})
            amount_to_deduct = amount_to_deduct_obj["amount"]

            if (int(user_balance)-int(amount_to_deduct)) <= user_balance and int(int(user_balance)-int(amount_to_deduct)) > 0:
                new_bal = int(user_balance)-int(amount_to_deduct)
                new_data = {"$set": {
                    "balance": new_bal
                }}
                data = {
                    "amount": 0
                }
                new_values = {"$set": data}
                amount_db.update_one({"current": "1"}, new_values)
                return {"isSuccess": "True", "details": {"balance": new_bal, "rfid": user_account["rfid"], "username": user_account["usrnme"]}}
            else:
                return {"isSuccess": "False", "msg": "Try Again"}
        else:
            return {"msg":"RFID not found"}
        

@app.route("/addClient", methods=["POST"])
def addClient():
    users = db['client_db_esp']
    user = request.json
    print(user)
    name = user['usrnme']
    phone = user['phone']
    pwd = bcrypt.generate_password_hash(user['pwd']).decode('utf-8')
    email = user['email']
    rfid = user['rfid']
    if users.find_one({"usrnme": name}) or users.find_one({"phone": phone}) or users.find_one({"email": email}):
        return {"isSuccess": "False", "msg": "Username or Phone number or Email already exist"}
    else:
        users.insert_one({
            'usrnme': name,
            'pwd': pwd,
            'email': email,
            "phone": phone,
            "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
            "balance": 0,
            "rfid": rfid
        })
        return {"isSuccess": "True", "msg": f"{name}'s data inserted", "details": {
            'usrnme': name,
            'pwd': pwd,
            'email': email,
            "phone": phone,
            "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
            "balance": 0,
            "rfid": rfid
        }}
    
@app.route("/deleteClient", methods=["DELETE"])
def deleteClient():
    users = db["client_db_esp"]
    rfid = request.args.get('rfid')
    if users.find_one({"rfid": rfid}) is None:
        return {"msg":f"{rfid} doesnot exists in the database"}

    users.delete_one({"rfid": rfid})
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    
@app.route("/addProduct", methods=["POST"])
def addProduct():
    users = db['product_db_esp']
    user = request.json
    print(user)
    productName = user['productName']
    productPrice = user['productPrice']
    pid =random.getrandbits(32)
    users.insert_one({
        'productName':productName,
        'productPrice':productPrice,
        "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
        "pid":pid
    })
    return {"isSuccess": "True", "msg": f"{productName}'s data inserted", "details": {
        'productName':productName,
        'productPrice':productPrice,
        "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
        "pid":pid
    }}


@app.route("/getAllProduct", methods=["GET"])
def getAllProduct():
    users = db["product_db_esp"]
    ans = []
    for user in users.find({}):
        ans.append({
        "productName": user['productName'],
        "productPrice": user['productPrice'],
        "pic_url": user['pic_url'],
        "pid":user['pid']
    })
    return ans

@app.route("/deleteProduct", methods=["DELETE"])
def deleteProduct():
    users = db["product_db_esp"]
    pid = request.args.get('pid')
    pid=int(pid)
    if users.find_one({"pid": pid}) is None:
        return {"msg":f"{pid} doesnot exists in the database"}

    users.delete_one({"pid": pid})
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route("/handlePayment", methods=["POST"])
def handlePayment():
    users = db['current_payment']
    user = request.json
    print(user)
    total_amount = user['total_amount']
    total_amount = int(total_amount)
    if users.find_one({"current": "1"}):
        data = {
            "amount":total_amount
        }
        new_values = {"$set": data}
        users.update_one({"current": "1"}, new_values)
        return {"msg":"Amount Updated", "total_amount":total_amount}
    else:
        return {"msg":"Amount not found"}
    
    
@app.route("/addbalance_esp", methods=["GET"])
def addbalance_esp():
    users = db["client_db_esp"]
    if request.method == "GET":  # and "usrnme" not in session:
        # user = request.json
        # name = user["usrnme"]
        rfid = request.args.get("rfid")
        addMoney = request.args.get("addMoney")
        # password = user["pwd"]
        logged_user = users.find_one({"rfid": rfid})
        print(logged_user)
        if logged_user:
            prev_bal = logged_user["balance"]
            if (int(prev_bal)+int(addMoney)) <= 20000:
                new_bal = int(prev_bal)+int(addMoney)
                new_data = {"$set": {
                    "balance": new_bal
                }}
                users.update_one({"rfid": rfid}, new_data)
                return {"isSuccess": "True", "details": {"balance": new_bal, "rfid": logged_user["rfid"]}}
            else:
                return {"isSuccess": "False", "msg": "Cannot add more than Rs 20,000"}
        else:
            return {"isSuccess": "False", "msg": "Invalid Data"}

# -------------------------------------------------------------------------------------------------------


@app.route("/logout")
def logout():
    name = request.args.get("usrnme")
    session.pop("usrnme", None)
    return f"{name.upper()} logged out successfully"


if __name__ == '__main__':
    app.run()
