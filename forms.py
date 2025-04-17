from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "name@example.com"})
    password = StringField('Password', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "abcd1234"})
    submit = SubmitField('Log In')


class CoffeeReviewForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    rating = FloatField('Rating(out of 10)', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    link = StringField('Link')
    img_url = StringField('Photo URL')
    submit = SubmitField('Submit')




