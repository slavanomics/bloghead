from flask import Flask, render_template
from flask_login import login_required, current_user
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from util import is_setup
from os import urandom
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = urandom(32)

class SetupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

toolbar = DebugToolbarExtension(app)

@app.route('/')
@is_setup
def index():
    return 'hi'

@app.route('/setup',methods=['GET','POST'])
def setup():
    form = SetupForm()
    if form.validate_on_submit():
        return redirect('/success')
    # do setup logic
    return render_template('setup.html',form=form)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000,ssl_context='adhoc')
 