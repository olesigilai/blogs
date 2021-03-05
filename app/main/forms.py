from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required
from ..models import User

class BlogsForm(FlaskForm):
    title = StringField('Blog Title')
    category = SelectField(u'Blog Categories', choices=[('Computing', 'Computing')])
    blog = TextAreaField('Blog')
    submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):
    comment = TextAreaField('Comment')
    submit = SubmitField('Post Comments')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Add Your profile.',validators = [Required()])
    submit = SubmitField('Submit')