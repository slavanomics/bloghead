from flask import Flask, render_template, redirect, flash
from flask.helpers import url_for
from flask_login import login_required, current_user
# im gonna use this comment space here to talk about some design goals with bloghead. the awful nature and consumerism of websites like medium and tumblr has driven me to write this program.
# because of that i wanna make it clear that my goal is to build something that is a) easy to deploy even for someone who doesn't know shit about computers b) easy to use for admins / day-to-day users
# my goal is in essence to have your own mini self hosted version of medium without it begging for your money every 2 minutes. 
# i'm not a big fan of hosted platforms and will always self-host when i have a chance, but no other blog platforms really did what i wanted to
# i guess some of this seems like rambling but its 2 am on a tuesday morning and i don't really care, i'm just leaving this in
# if you're developing a plugin / theme / fork or something for bloghead, these are things you should probably understand when it comes to my design philosophy
from models import db, User
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,IntegerField
from wtforms.validators import DataRequired, NumberRange
from util import is_setup
from os import urandom, path
import configparser

config = configparser.ConfigParser()
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = urandom(32)

if path.exists('config.ini'):
    config.read('config.ini')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('Database','DB_URI') #kill me tbh 

db.init_app(app)
class SetupForm(FlaskForm): #TODO move this form and make other forms in forms.py
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
            uri = f'mariadb+mariadbconnector://{form.dbuser.data}:{form.dbpass.data}@{form.dbhost.data}:{form.dbport.data}/{form.dbname.data}'
            app.config['SQLALCHEMY_DATABASE_URI'] = uri # TODO@slavanomics add select in form and make this work with engines other than mariadb.
            db.create_all()
            # generate config once database table generation went successfully
            # for now im going to just make this store the uri from above, once i implement sources other than MariaDB i will change the way the config file is structured.
            config['Database'] = {'DB_URI': uri}
            with open('config.ini','w') as configfile:
                config.write(configfile)
        except Exception as e:
            flash(str(e))
            return render_template('setup.html',form=form)
        return render_template('success.html')
    # do setup logic
    return render_template('setup.html',form=form)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000,ssl_context='adhoc')
 