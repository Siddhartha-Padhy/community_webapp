import json
import pyrebase
import datetime

# Get the firebase configurations
def firebaseConfigRead():
    with open("fireConfig.json", 'r') as f:
        return json.load(f)

def getSecretKey():
    with open("secret.txt", 'r') as f:
        return f.read()

firebaseConfig = firebaseConfigRead()
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# Initialize user's portfolio with it's username
def create_user_database(username):
    data = {
        'Username': username
    }
    db.child('Community').child('Users').push(data)

# Check whether the username exists or not
def validate_username(username):
    copies = db.child('Community').child('Users').order_by_child('Username').equal_to(username).get()
    for copy in copies.each():
        if copy.val() != None:
            return False
    return True

# Add a post to user's database having Content, Date and Time attributes
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

# Get a post from user's database. Attributes: Content, Date and Time
def get_posts(username):
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

# Set the status of a user
def set_status(username,status):
    curr_user = db.child('Community').child('Users').order_by_child('Username').equal_to(username).get()

    for user in curr_user.each():
        if user.val()['Username'] == username:
            status = db.child('Community').child('Users').child(user.key()).update({'Status':status})

# Get the status of a user
def get_status(username):
    curr_user = db.child('Community').child('Users').order_by_child('Username').equal_to(username).get()

    for user in curr_user.each():
        if user.val()['Username'] == username:
            status_list = db.child('Community').child('Users').child(user.key()).get()
            try:
                return status_list.val()['Status']
            except:
                return 'Hello there!'

# Add a user to logged in user's database
def follow_user(username,follow_username):
    curr_user = db.child('Community').child('Users').order_by_child('Username').equal_to(username).get()

    for user in curr_user.each():
        if user.val()['Username'] == username:
            db.child('Community').child('Users').child(user.key()).child('Following').push({ 'Username': follow_username })

# Get the users followed by the logged in user
def get_following(username):
    curr_user = db.child('Community').child('Users').order_by_child('Username').equal_to(username).get()

    for user in curr_user.each():
        if user.val()['Username'] == username:
                followings = db.child('Community').child('Users').child(user.key()).child('Following').get()

    result = []
    try:
        for following in followings.each():
            result.append(following.val()['Username'])
    except:
        pass
    return result