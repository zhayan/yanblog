from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, Length

class CommentForm(FlaskForm):
	nickname = StringField('Nickname', validators=[DataRequired()])
	email = StringField('Email', validators=[Email()])
	comment = TextAreaField('Comment', validators=[DataRequired()])
	submit = SubmitField('Submit')

