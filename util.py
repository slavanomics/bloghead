from os import path
from functools import wraps

from flask import flash, redirect, url_for


def is_setup(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not path.exists('config.ini'):
            flash("You have not completed the setup!")
            return redirect(url_for('setup'))
        return func(*args, **kwargs)

    return decorated_function