from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, DecimalField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from wtforms import FileField

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class PaymentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    document = FileField('Document')
    submit = SubmitField('Create Request')

class DocumentsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Create Request')

class PurchaseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField('Create Request')

class GoalsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Create Request')

class CategoryForm(FlaskForm):
    category = SelectField('Category', choices=[('payment', 'Payment'), ('documents', 'Internal Documents'), ('purchase', 'Purchase Request'), ('goals', 'Goals/Assignments')], validators=[DataRequired()])
    submit = SubmitField('Next')

