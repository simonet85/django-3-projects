from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

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

@register.simple_tag 
def get_most_commented_post( count=5 ) :
    return Post.published.annotate(
        total_comments = Count('comments')
    ).order_by('-total_comments')[:count]
    
#Custom template filters
@register.filter( name='markdown' )
def markdown_format( text ) :
    return mark_safe( markdown.markdown( text ))