from django import template
from ..models import Post

register = template.Library()
#create simple template tag simple_tag
@register.simple_tag
def total_posts() :
    return Post.published.count()

#create template inclusion inclusion_tag
@register.inclusion_tag( 'blogsite/post/latest_posts.html' )
def show_latest_posts( count=5 ) :
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts' : latest_posts}