from flask import Flask, request, render_template, redirect, url_for, session
import requests,json
import pyrebase

config = {
  "apiKey": "AIzaSyB_-k452y32DZDY5oQR63M5BRHI3ox2SGo",
  "authDomain": "y2-task.firebaseapp.com",
  "projectId": "y2-task",
  "storageBucket": "y2-task.appspot.com",
  "messagingSenderId": "795849119492",
  "appId": "1:795849119492:web:c75dadb4570920178ca251",
  "measurementId": "G-54PEG5238N",
  "databaseURL": "https://y2-task-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask( 
	__name__,
	template_folder='templates', 
	static_folder='static'  
) 
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
@app.route('/',methods=['GET', 'POST'])  
def login():
  if request.method == 'GET':
    return render_template('login.html')
  else:
    email = request.form['email']
    password = request.form['password']
    try:
      session['user'] = auth.sign_in_with_email_and_password(email, password)
      return redirect(url_for('home'))
    except:
      error = "Authentication failed"
      return render_template('login.html', error=error)
ball_api = requests.get("https://www.balldontlie.io/api/v1/games")
parsed_json = json.loads(ball_api.content)
games = parsed_json['data']

@app.route('/home',methods=['GET', 'POST'])  
def home():
  if request.method == 'GET':
    return render_template('home.html')
  else:
    return render_template('home.html', games=games)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    return render_template('signup.html')
  else:
    error = ""
    email = request.form['email']
    password = request.form['password']
    try:
      session['user'] = auth.create_user_with_email_and_password(email, password)
      user = {"email": email, "password": password}
      db.child("Users").child(session['user']['localId']).set(user)
      return redirect(url_for('login'))
    except:
      error = "Authentication failed"
    return render_template('signup.html', error=error)
@app.route('/logout')
def logout(): 
  session['user'] = None
  auth.current_user = None
  return redirect(url_for('login'))

if __name__ == "__main__":
	app.run(
		host='0.0.0.0', 
		port=5000, 
    debug=True
	)