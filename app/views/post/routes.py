import delta
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Post, Category, Tag
from app.forms import PostForm, EditPostForm
from app.utils import user_has_capability
from app.views.post import post_bp
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import bleach
from bleach.css_sanitizer import CSSSanitizer
from delta import Delta, html
from slugify import slugify

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'ogg'}
#post_bp = Blueprint('post', __name__, url_prefix='/post')

ALLOWED_TAGS = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'ul', 'ol', 'li', 'br', 'a', 'img', 'span', 'div', 'table', 'tbody', 'td', 'th', 'thead']
ALLOWED_ATTRIBUTES = {
    '*': ['class', 'style'],
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'width', 'height'],
}
ALLOWED_STYLES = [
    'background-color', 'color', 'font-family', 'font-size', 'font-style',
    'font-weight', 'text-align', 'text-decoration', 'vertical-align',
    'padding-left', 'padding-right', 'padding-top', 'padding-bottom',
    'margin-left', 'margin-right', 'margin-top', 'margin-bottom',
    'line-height', 'width', 'height', 'border', 'border-style', 'border-color'
]
css_sanitizer = CSSSanitizer(allowed_css_properties=ALLOWED_STYLES)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@post_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return url_for('static', filename='uploads/' + filename), 200
    return 'Not allowed file type', 400

@post_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if not user_has_capability(current_user, 'create_post'):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        content = form.content.data or ""
        css_santizer = CSSSanitizer(allowed_css_properties=ALLOWED_STYLES)
        cleaned_content = bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, css_sanitizer=css_santizer, strip=True)
        html_content = cleaned_content
        post = Post(title=form.title.data, content=html_content, status=form.status.data, author=current_user) 
        post.generate_slug()
        selected_categories = form.categories.data
        post.categories.extend(Category.query.filter(Category.id.in_(selected_categories)).all())
        
        tags_string = form.tags.data
        if tags_string:
            tag_names = [tag.strip() for tag in tags_string.split(',')]
            for tag_name in tag_names:
                slug = slugify(tag_name)
                tag = Tag.query.filter_by(slug=slug).first()
                if not tag:
                    tag = Tag(name=tag_name, slug=slug)
                    db.session.add(tag)
                post.tags.append(tag)
        try:
            db.session.add(post)
            db.session.commit()
            flash('Post created!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            print(f"Error saving post: {e}")
            flash("An error occurred while saving the post.", "danger")
    return render_template('post/create_post.html', form=form)


@post_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not user_has_capability(current_user, 'edit_post'):
        abort(403)

    form = EditPostForm(obj=post)
    show_approval = user_has_capability(current_user, 'publish_post')

    if form.validate_on_submit():
        form.populate_obj(post)
        if form.categories.data:
            post.categories = [Category.query.get(int(category_id)) for category_id in form.categories.data]
        if form.tags.data:
            tags_string = form.tags.data
            tag_names = [tag.strip() for tag in tags_string.split(',')]
            for tag_name in tag_names:
                slug = slugify(tag_name)
                tag = Tag.query.filter_by(slug=slug).first()
                if not tag:
                    tag = Tag(name=tag_name, slug=slug)
                    db.session.add(tag)
                post.tags.append(tag)
        content = form.content.data
        cleaned_content = bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, css_sanitizer=css_sanitizer, strip=True)
        post.content = cleaned_content
        post.generate_slug()

        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('post.view_post', slug=post.slug))

    return render_template('post/edit_post.html', form=form, post=post, show_approval=show_approval)


@post_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not user_has_capability(current_user, 'delete_post'):
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('main.manage_posts'))

@post_bp.route('/<slug>')
def view_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('post/view_post.html', post=post, content=post.content) # Directly pass the content