from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, SubmitField, validators, ValidationError, TextField, SubmitField
from flask_pagedown.fields import PageDownField



class ContactForm(FlaskForm):
    name = StringField("Name", [validators.Required("Please enter your name before submitting.")])
    email = StringField("Email", [validators.Required("Please enter your email address before submitting.")])
    subject = StringField("Subject", [validators.Required("Please enter a subject before submitting.")])
    message = TextAreaField("Message", [validators.Required("Please enter the body of your message before submitting.")])
    submit = SubmitField("Send")
    
    
class NoteForm(FlaskForm):
    
    note_title = TextField('Note Title:', [validators.Required("Please enter \
      a note title.")])
    note_body = TextAreaField('Your Note:')
    submit = SubmitField('Add Note')

class PageDownFormExample(Form):
    pageDown = PageDownField('Enter your markdown')
    submit = SubmitField('Submit')

