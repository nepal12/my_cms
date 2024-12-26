from flask import abort, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils import user_has_capability
from app.views.main import main_bp
from app import db
from app.models import User, Post

from app.forms import EditUserForm  # Import EditUserForm
from app.utils import ROLES, user_has_capability, create_excerpt
 
@main_bp.route('/')
def index():
    posts = Post.query.filter_by(status='published', approved=True).order_by(Post.date_posted.desc()).all() #Added order_by
    return render_template('index.html', posts=posts, create_excerpt=create_excerpt)


@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/admin')
@login_required
def admin_panel():
    if not user_has_capability(current_user, 'access_admin_panel'):
        abort(403)  # Forbidden
    return render_template('admin/panel.html')

@main_bp.route('/users')
@login_required
def manage_users():
    if not user_has_capability(current_user, 'manage_users'):
        abort(403)
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@main_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not user_has_capability(current_user, 'manage_users'):
        abort(403)
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user) # Prefill the form
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.commit()
        flash('User role updated.', 'success')
        return redirect(url_for('main.manage_users'))
    return render_template('admin/edit_user.html', user=user, roles=ROLES.keys(), form=form)

@main_bp.route('/admin/posts')
@login_required
def manage_posts():
    if not user_has_capability(current_user, 'manage_posts'):
        abort(403)
    posts = Post.query.all()
    return render_template('admin/manage_posts.html', posts=posts)