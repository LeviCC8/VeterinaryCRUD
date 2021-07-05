from flask import flash
from flask_login import login_user


def flash_form_errors_messages(form, default_message):
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{default_message}: {err_msg}', category='danger')


def login_user_in_system(user, default_message):
    login_user(user)
    flash(default_message, category='success')
