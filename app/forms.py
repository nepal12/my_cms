from flask_wtf import FlaskForm
from slugify import slugify
from wtforms import SelectMultipleField, StringField, PasswordField, SubmitField, EmailField, SelectField, BooleanField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import Tag
from app.utils import ROLES
from app.models import Category
from app import db

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EditUserForm(FlaskForm):
    role = SelectField('Role', choices=[(role, role.capitalize()) for role in ROLES.keys()], validators=[DataRequired()])
    submit = SubmitField('Update Role')

POST_STATUSES = [('draft', 'Draft'), ('published', 'Published'), ('trashed', 'Trashed')]

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content') 
    status = SelectField('Status', choices=POST_STATUSES, validators=[DataRequired()])
    categories = SelectMultipleField('Categories', coerce=int) # Coerce to int for category IDs
    tags = StringField('Tags (comma-separated)')
    submit = SubmitField('Submit')
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.categories.choices = [(c.id, c.name) for c in Category.query.all()]

class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')
    status = SelectField('Status', choices=[('draft', 'Draft'), ('published', 'Published')], validators=[DataRequired()])
    categories = SelectMultipleField('Categories', coerce=int)  # Coerce to int
    tags = StringField('Tags (comma-separated)')
    approved = BooleanField('Approved')
    submit = SubmitField('Update Post')

    def __init__(self, post=None, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        self.categories.choices = [(c.id, c.name) for c in Category.query.all()]
        if post:
            self.categories.data = [c.id for c in post.categories]
            self.tags.data = ', '.join(tag.name for tag in post.tags)
    
    def update_post(self, post):
        post.title = self.title.data
        post.content = self.content.data
        post.status = self.status.data
        post.approved = self.approved.data

        post.categories = [Category.query.get(int(category_id)) for category_id in self.categories.data if self.categories.data]

        post.tags = []
        submitted_tags = [tag.strip() for tag in self.tags.data.split(',') if tag.strip()]
        for tag_name in submitted_tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, slug=slugify(tag_name))
                db.session.add(tag)
            post.tags.append(tag)

        return post
        
class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TagForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')