from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '881e75131983b16650ecd36fd815997e';
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db';
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/register', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    registration_form = RegistrationForm()
    return render_template('index.html', login_form=login_form, registration_form=registration_form)

if __name__ == '__main__':
    app.run(debug=True)
