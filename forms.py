from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, SubmitField, validators, ValidationError

class ContactForm(Form):
    name = StringField("Name", [validators.Required("Please enter your name before submitting.")])
    email = StringField("Email", [validators.Required("Please enter your email address before submitting.")])
    subject = StringField("Subject", [validators.Required("Please enter a subject before submitting.")])
    message = TextAreaField("Message", [validators.Required("Please enter the body of your message before submitting.")])
    submit = SubmitField("Send")
