from flask import Flask, render_template, redirect, flash
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,IntegerField
from wtforms.validators import DataRequired, NumberRange
from util import is_setup
from os import urandom, path
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = urandom(32)

if path.exists('setup.ini'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)
class SetupForm(FlaskForm):
    dbuser = StringField('User', validators=[DataRequired()])
    dbpass = PasswordField('Password', validators=[DataRequired()])
    dbhost = StringField('Host', validators=[DataRequired()])
    dbport = IntegerField('Port', validators=[DataRequired(),NumberRange(0,65535,"That's an impossible port!")])
    dbname = StringField('Database Name',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

toolbar = DebugToolbarExtension(app)

@app.route('/')
@is_setup
def index():
    return 'hi'

@app.route('/setup',methods=['GET','POST'])
def setup():
    form = SetupForm()
    if form.validate_on_submit():
        try:
            # test sql connection before comitting to file
            # construct sqlalchemy uri
            app.config['SQLALCHEMY_DATABASE_URI'] = f'mariadb+mariadbconnector://{form.dbuser.data}:{form.dbpass.data}@{form.dbhost.data}:{form.dbport.data}/{form.dbname.data}' # TODO@slavanomics add select in form and make this work with engines other than mariadb.
            db.create_all()
        except Exception as e:
            flash(str(e))
            return render_template('setup.html',form=form)
        return "t"
    # do setup logic
    return render_template('setup.html',form=form)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000,ssl_context='adhoc')
 