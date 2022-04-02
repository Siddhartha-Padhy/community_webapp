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
    date = datetime.datetime.now().strftime('%d %b %Y')
    time = datetime.datetime.now().strftime('%I:%M %p')
    data = {
        'Content': content,
        'Date': date,
        'Time': time
    }
    curr_user = db.child('Community').child('Users').order_by_child('Username').equal_to(username).get()

    for user in curr_user.each():
        if user.val()['Username'] == username:
            db.child('Community').child('Users').child(user.key()).child('Posts').push(data)

def get_personal_posts(username):
    curr_user = db.child('Community').child('Users').order_by_child('Username').equal_to(username).get()

    results = []
    for user in curr_user.each():
        if user.val()['Username'] == username:
            posts = db.child('Community').child('Users').child(user.key()).child('Posts').get()
    
    try:
        for post in posts.each():
            result = {}
            result['Content'] = post.val()['Content']
            result['Time'] = post.val()['Time']
            if post.val()['Date'] == str(datetime.datetime.now().strftime('%d %b %Y')):
                result['Date'] = 'Today'
            else:
                result['Date'] = post.val()['Date']
            results.append(result)
    except:
        pass

    return results

def set_status(username,status):
    curr_user = db.child('Community').child('Users').order_by_child('Username').equal_to(username).get()

    for user in curr_user.each():
        if user.val()['Username'] == username:
            status = db.child('Community').child('Users').child(user.key()).update({'Status':status})

def get_personal_status(username):
    curr_user = db.child('Community').child('Users').order_by_child('Username').equal_to(username).get()

    for user in curr_user.each():
        if user.val()['Username'] == username:
            status_list = db.child('Community').child('Users').child(user.key()).get()
            return status_list.val()['Status']
