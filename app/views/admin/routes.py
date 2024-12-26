from flask import render_template, request, redirect, url_for, flash
from . import admin_bp
from app.models import Category, Tag, Post
from app.extensions import db
from app.forms import CategoryForm, TagForm # Create these forms later
from slugify import slugify

# Category Views
@admin_bp.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        slug = slugify(form.name.data)
        category = Category(name=form.name.data, slug=slug)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully.', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/add_category.html', form=form)

@admin_bp.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        category.slug = slugify(form.name.data)
        db.session.commit()
        flash('Category updated successfully.', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/edit_category.html', form=form)

@admin_bp.route('/categories/delete/<int:id>')
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully.', 'success')
    return redirect(url_for('admin.categories'))

# Tag Views (Similar structure)
@admin_bp.route('/tags')
def tags():
    tags = Tag.query.all()
    return render_template('admin/tags.html', tags=tags)

@admin_bp.route('/tags/add', methods=['GET', 'POST'])
def add_tag():
    form = TagForm()
    if form.validate_on_submit():
        slug = slugify(form.name.data)
        tag = Tag(name=form.name.data, slug=slug)
        db.session.add(tag)
        db.session.commit()
        flash('Tag added successfully.', 'success')
        return redirect(url_for('admin.tags'))
    return render_template('admin/add_tag.html', form=form)

@admin_bp.route('/tags/edit/<int:id>', methods=['GET', 'POST'])
def edit_tag(id):
    tag = Tag.query.get_or_404(id)
    form = TagForm(obj=tag)
    if form.validate_on_submit():
        tag.name = form.name.data
        tag.slug = slugify(form.name.data)
        db.session.commit()
        flash('Tag updated successfully.', 'success')
        return redirect(url_for('admin.tags'))
    return render_template('admin/edit_tag.html', form=form)

@admin_bp.route('/tags/delete/<int:id>')
def delete_tag(id):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted successfully.', 'success')
    return redirect(url_for('admin.tags'))
