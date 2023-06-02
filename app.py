from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL, Email
from data import QUESTIONS
from duration import *
import time
from datetime import timedelta
from sqlalchemy.exc import IntegrityError



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
csfr = CSRFProtect(app)
Bootstrap(app)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours= 24)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

TODAY = time.localtime()
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", TODAY)



#CONFIGURE TABLE
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250))


##WTForm
class Register(FlaskForm):
    name = StringField("", validators=[DataRequired()])
    email = EmailField("", validators=[DataRequired(), Email()])
    password = PasswordField("", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    
class Login(FlaskForm):
    email = EmailField("", validators=[DataRequired(), Email()])
    password = PasswordField("", validators=[DataRequired()])
    submit = SubmitField("Sign In")

class Subject_form(FlaskForm):
    submit = SubmitField("")


CHOSED_SUBJECTS = list()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/exam', methods=['POST', 'GET'])
def exam():
    if "user_session" in session:
        form = Subject_form()
        Selected = False
        global CHOSED_SUBJECTS
        if request.method == 'POST':
            subjects = request.form.getlist('options')
            if len(subjects) == 3:
                Selected = True
                CHOSED_SUBJECTS.append(subjects)
                # for _ in range(1, 3):
                #     for sub in subjects:
                #         QUES = QUESTIONS(sub)
                #         QUES.fetch_questions()
            elif len(subjects) == 0:
                flash('Please select your subjects')
            else:
                flash('You can only pick 3 subjects')
        return render_template("exam.html", select=Selected, form=form)
    else:
        return redirect(url_for('login'))
    

    

@app.route('/ongoing-exam', methods=['POST'])
def ongoing_exam():
    if "user_session" in session:
        current_sub = str(CHOSED_SUBJECTS[0])
        Que = QUESTIONS(current_sub)
        DATA_LOG = Que.load_question()
        TIMING = countdown_timer(300)
        Start = False
        form = Subject_form()
        question = 1
        if request.method == 'POST':
            Start = True
            
        return render_template('ongoing.html', DATA_LOG=DATA_LOG, TIMING=TIMING, start=Start,form=form, question=question)
    else:
        return redirect(url_for('login'))


@app.route('/about')
def about():
    if "user_session" in session:
        return render_template('about.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/contact')
def contact():
    if "user_session" in session:
        return render_template('contact.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = Login()
    isLogged = False
    if login_form.validate_on_submit():
        app.permanent_session = True
        user_session = login_form.email.data
        session['user_session'] = user_session
        load_user = User.query.filter_by(email=login_form.email.data, password=login_form.password.data)
        if load_user:
            flash('Logged In Succesfully')
            isLogged = True
            return redirect(url_for('profile'))
        else:
            flash("User does'nt exists")
    else:
        if 'user_session' in session:
            return redirect(url_for('profile'))


    return render_template("login.html", form=login_form, isLogged=isLogged)





@app.route('/register', methods=['GET', 'POST'])
def register():
    if "user_session" not in session:
        register_form = Register()
        if register_form.validate_on_submit():
            load_user = User.query.filter_by(email=register_form.email.data)
            if load_user:
                flash('Email already exists')

            else:
                try:
                    new_data = User(
                        name=register_form.name.data,
                        email=register_form.email.data,
                        password=register_form.password.data,
                        date=formatted_time,

                    )
                    db.session.add(new_data)
                    db.session.commit()
                
                except IntegrityError:
                    db.session.rollback()

                return redirect(url_for('login'))
    
        return render_template("register.html", form=register_form)
    
    else:
        return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    if 'user_session' in session:
        return render_template('profile.html')
    else:
        return redirect('login')

@app.route('/logout')
def logout():
    session.pop('user_session', None)
    flash("User logged out")
    return redirect(url_for('home'))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)