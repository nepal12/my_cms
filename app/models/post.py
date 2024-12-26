from app.extensions import db
from datetime import datetime, timezone
from slugify import slugify
from .category import Category
from .tag import Tag
from .association_tables import post_categories, post_tags

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=True)  # Store as plain HTML
    categories = db.relationship('Category', secondary='post_categories', backref=db.backref('posts', lazy=True))
    tags = db.relationship('Tag', secondary='post_tags', backref=db.backref('posts', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    date_posted = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='draft')
    approved = db.Column(db.Boolean, default=False)
    approved_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    approved_by = db.relationship('User', foreign_keys=[approved_by_id], backref='approved_posts')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True), foreign_keys=[author_id])

    def generate_slug(self):
        self.slug = slugify(self.title)

    def get_content(self):
        return self.content or ""  # Return content or empty string if None

    def set_content(self, content):
        self.content = content

    def __repr__(self):
        return f'<Post {self.title}>'