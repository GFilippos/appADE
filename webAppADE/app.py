from flask import Flask,render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from datetime import timedelta
import nominatim
from geopy import Nominatim
from unidecode import unidecode
from nominatim import reverseGeo
import requests 

app = Flask(__name__)

#adding the database
db= SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 's3cr3tk3!'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# app.permanent_session_lifetime = timedelta(minutes=5)

#hash password
bcrypt = Bcrypt(app)


#user login handling
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#create db Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(24), nullable=False)
    # latitude = db.Column(db.Float(40))
    # longitude = db.Column(db.Float(40))


class RegisterForm(FlaskForm):
    username = StringField  (validators = [InputRequired(), Length(min = 6, max = 12)], render_kw={"placeholder" : "Username"})
    password = PasswordField(validators = [InputRequired(), Length(min = 6, max = 12)], render_kw={"placeholder" : "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username = username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField  (validators = [InputRequired(), Length(min = 6, max = 12)], render_kw={"placeholder" : "Username"})
    password = PasswordField(validators = [InputRequired(), Length(min = 6, max = 12)], render_kw={"placeholder" : "Password"})
    submit = SubmitField("Login")


#my routes
@app.route("/", methods = ['POST', 'GET'])
def index():
    return render_template('sidebar.html')

@app.route("/home", methods = ['POST', 'GET'])
def home():
    if "user" in session:
        return redirect(url_for('dashboard'))
    return render_template('sidebar.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                session["user"] = user.username
                return redirect(url_for('dashboard'))
            else:
                flash("The password you entered is incorrect", "error")
                return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)

@app.route("/register", methods = ['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username = form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/dashboard", methods = ['POST', 'GET'])
@login_required
def dashboard():
    user = session["user"]
    flash(f"Hello {user} Welcome!", "info")
    return render_template('dashboard.html', user=user)

@app.route("/logout" , methods = ['POST', 'GET'])
@login_required
def logout():
    user = session["user"]
    flash(f"You have logged out successfully {user}!", "info") 
    logout_user()
    session.pop("user", None)  
    return redirect(url_for('home'))

@app.route("/project", methods = ['POST', 'GET'])
@login_required
def project():
    return render_template('project.html')

@app.route("/distance", methods = ['POST', 'GET'])
def distance():
    return render_template('distance.html')

@app.route("/country", methods = ['POST', 'GET'])
def country():
    user_pos = request.json()
    print(user_pos)
    country, user_info = reverseGeo(user_pos)
    #session['userData'] = user_data 
    # user_data function
    # country = nominatim.countryN 
    # user_info = nominatim.user_info
    return render_template('country.html', country=country, user_info=user_info)


if __name__ == '__main__':
    app.run(debug=True)

