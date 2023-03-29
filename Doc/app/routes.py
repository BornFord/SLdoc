from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from app.models import db
from app.forms import LoginForm, RegistrationForm, PaymentForm, DocumentsForm, PurchaseForm, GoalsForm
from app.models import User, Request, Recipient

bp = Blueprint('routes', __name__)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    active_requests = current_user.requests.all()
    return render_template('home.html', title='Home', active_requests=active_requests)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('routes.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('routes.index'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


#@bp.route( '/category', methods=['GET', 'POST'] )
#def category():
#    if ConnectionRefusedError.((compile)