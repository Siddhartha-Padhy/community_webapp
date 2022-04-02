# :two_men_holding_hands: Community Webapp
*Thoughtful* is a community web app built with Python-Django and Firebase realtime database to share your thoughts.

## :sparkles: Features
This app provides platform for everyone to post their thoughts and read other's posts.
- All the recent posts are shown on the home page.
- Follow other users so that you don't miss out their posts.
- Explore users and see their profile and what they think.
- Know the trending thought makers.

## ⚙ Requirements
Install the dependencies using ```pip install -r requirements.txt```
A firebase realtime database is required.<br>
Firebase configurations are stored in JSON format in fireConfig.json in the main directory.

## 💻 Installation and Running
Run ```python manage.py runserver``` to get the server up and running.<br>
Open a web browser and go to ```localhost:8000``` then Sign up or login and get started.<br>
To create a super user use the following command and pass the required values.
```
python manage.py createsuperuser
Username: /*Your username here*/
Email address: /*Your email address here*/
Password: /*Your Password*/
Password (again): /*Your Password*/
Superuser created successfully.
```

## 📚 Resources
- [Firebase Realtime Database Documentation](https://firebase.google.com/docs/database)
- [Pyrebase Repository](https://github.com/thisbejim/Pyrebase)
- [Django Documentation](https://docs.djangoproject.com/en/4.0/contents/)

<img src="https://i0.wp.com/copyassignment.com/wp-content/uploads/2021/08/Django-logo.jpg?fit=474%2C474&ssl=1" width=10%>&nbsp;<img src="https://firebase.google.com/images/brand-guidelines/logo-built_white.png" width=20%>
