from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField,ValidationError
from wtforms.validators import Required
from ..models import User,Subscriber

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

class SubscriberForm(FlaskForm):
    email = TextAreaField('enter your valid email address.',validators = [Required()])
    username = TextAreaField('username', validators = [Required()])
    submit = SubmitField('Submit')

    def validate_email(self,data_field):
        if Subscriber.query.filter_by(email = data_field.data).first():
            raise ValidationError('Your data already exists') 