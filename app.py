from flask import Flask, render_template, redirect, url_for, flash, request
from db import db
from forms import RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.user import User
from models.post import Post
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '881e75131983b16650ecd36fd815997e';
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db';
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    """Login or Register Page"""
    # If user logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    show_form = 'login' if request.args.get('show_form') == 'login' else 'register'
    registration_form = RegistrationForm()
    login_form = LoginForm()
    if registration_form.validate_on_submit():
        flash('Thanks for registering')
        user = User.query.filter((User.username==registration_form.username.data) | (User.email==registration_form.email.data)).first()
        if not user:
            hashed_password = generate_password_hash(registration_form.password.data)
            new_user = User(username=registration_form.username.data, fullname=registration_form.fullname.data, email=registration_form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index', show_form='login'))
        return '<h1>Username or Email has been used!</h1>'
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user:
            if check_password_hash(user.password, login_form.password.data):
                login_user(user, remember=login_form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1>Invalid username or password!</h1>'
    return render_template('index.html', registration_form=registration_form, login_form=login_form, show_form=show_form)

@app.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/profile/<string:username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
