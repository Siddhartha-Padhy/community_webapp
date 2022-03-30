import json
import pyrebase
import datetime

def firebaseConfigRead():
    with open("fireConfig.json", 'r') as f:
        return json.load(f)

def getSecretKey():
    with open("secret.txt", 'r') as f:
        return f.read()

firebaseConfig = firebaseConfigRead()
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def create_user_database(username):
    data = {
        'Username': username
    }
    db.child('Community').child('Users').push(data)

def validate_username(username):
    copies = db.child('Community').child('Users').order_by_child('Username').equal_to(username).get()
    for copy in copies.each():
        if copy.val() != None:
            return False
    return True

def make_post(username,content):
    if content =="":
        return
    time = datetime.datetime.now().strftime('%d-%b-%Y  %I-%M %p')
    data = {
        'Content': content,
        'Time': time
    }
    curr_user = db.child('Community').child('Users').order_by_child('Username').equal_to(username).get()

    for user in curr_user.each():
        if user.val()['Username'] == username:
            db.child('Community').child('Users').child(user.key()).child('Posts').push(data)