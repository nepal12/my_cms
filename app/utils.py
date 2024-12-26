import  bleach
from bleach.css_sanitizer import CSSSanitizer

ROLES = {
    'superadmin': {
        'capabilities': ['create_post', 'edit_post', 'delete_post', 'publish_post', 'manage_users', 'manage_categories', 'access_admin_panel', 'manage_posts']
    },
    'admin': {
        'capabilities': ['create_post', 'edit_post', 'delete_post', 'publish_post', 'manage_categories', 'manage_posts']
    },
    'editor': {
        'capabilities': ['create_post', 'edit_post', 'publish_post']
    },
    'author': {
        'capabilities': ['create_post', 'edit_post']
    },
    'contributor': {
        'capabilities': ['create_post']
    }
}

ALLOWED_EXCERPT_TAGS = ['p', 'br', 'strong', 'em', 'u', 'i', 'span', 'a', 'ul', 'ol', 'li', 'blockquote','pre','h1', 'h2', 'h3', 'h4', 'h5',
    'h6', 'b', 'font']
ALLOWED_EXCERPT_ATTRIBUTES = {
    'a': ['href', 'title', 'target'],
    'span': ['style']
}
ALLOWED_EXCERPT_STYLES = ['color', 'font-weight', 'font-style', 'text-decoration', 'background-color']
css_sanitizer = CSSSanitizer(allowed_css_properties=ALLOWED_EXCERPT_STYLES)


def user_has_capability(user, capability):
    if user and user.role in ROLES and capability in ROLES[user.role]['capabilities']:
        return True
    return False

def create_excerpt(html_content, max_length=50, by_words=True):
    """Creates an excerpt from HTML content, preserving basic formatting."""
    if not html_content:
        return ""

    if by_words:
        text = bleach.clean(html_content, tags=ALLOWED_EXCERPT_TAGS, attributes=ALLOWED_EXCERPT_ATTRIBUTES, css_sanitizer=css_sanitizer, strip=False)
        words = text.split()
        if len(words) <= max_length:
            return text
        excerpt = " ".join(words[:max_length]).strip() + "..."
    else:
        text = bleach.clean(html_content, tags=ALLOWED_EXCERPT_TAGS, attributes=ALLOWED_EXCERPT_ATTRIBUTES, css_sanitizer=css_sanitizer, strip=False)
        if len(text) <= max_length:
            return text
        excerpt = text[:max_length].strip() + "..."
        
    return excerpt