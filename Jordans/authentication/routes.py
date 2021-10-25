from flask import Blueprint, render_template, request,url_for, flash, redirect
from Jordans.forms import UserLoginForm
from Jordans.models import User, db, check_password_hash
from flask_login import login_user, login_required, logout_user


auth = Blueprint('auth',__name__,template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)
        new_user = User(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'You have successfully registered an account under{email}', 'user-created')
        return redirect(url_for('site.home'))
        


    return render_template('signup.html', form = form)


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)

        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash('You were successfully logged in')
            return redirect(url_for('site.home'))

        else:
            flash('Your Email/Password id incorrent')
            return redirect(url_for('auth.signin'))


    return render_template('signin.html', form = form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out.')
    return redirect(url_for('site.home'))
