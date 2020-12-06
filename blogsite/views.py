from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
 
def post_list( request, tag_slug=None ) :
    #posts = Post.published.all()
    object_list = Post.published.all()
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter( tags__in=[tag] )
    paginator = Paginator( object_list, 3 ) # 3posts in each in each page
    page = request.GET.get( 'page' ) #page Number
    try:
        posts = paginator.get_page( page ) #page Object
    except PageNotAnInteger :
        #If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage :
        #If page is out of range deliver last page of results
        posts = paginator.page( paginator.num_pages )
   
    return render( request,
                  'blogsite/post/list.html',
                  {'page':page,'posts' : posts,'tag' : tag} 
                  )

def post_detail( request, year, month, day, post ) :
    post = get_object_or_404(Post, slug=post, status = 'published', publish__year = year, publish__month = month, publish__day = day)
    
    #List of similar posts
    #Retrieve all tags for the current post
    #.1 You retrieve a Python list of IDs for the tags of the current post. The values_list() QuerySet returns tuples with the values for the given fields. You pass flat=True to it to get single values such as [1, 2, 3, ...] instead of one-tuples such as [(1,), (2,), (3,) ...].
    post_tags_ids = post.tags.values_list( 'id', flat=True )
    #Exclude the current post from that list to avoid recommending the same post
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude( id=post.id )
    #You use the Count aggregation function to generate a calculated field—same_tags—that contains the number of tags shared with all the tags queried.
    similar_posts = similar_posts.annotate( same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    #You order the result by the number of shared tags (descending order) and by publish to display recent posts first for the posts with the same number of shared tags. You slice the result to retrieve only the first four posts.
    comments = post.comments.filter( active=True )
    new_comment = None
    if request.method == 'POST' :
        #A comment was posted
        comment_form = CommentForm( data=request.POST )
        if comment_form.is_valid() :
            #Create Comment object but don't save to databse yet
            new_comment = comment_form.save( commit=False )
            #Assign the current post to the comment
            new_comment.post = post
            #Save the comment to the database
            new_comment.save()
    else :
        comment_form = CommentForm()
    return render( request, 'blogsite/post/detail.html', {
        'post' : post, 
        'comments': comments, 
        'new_comment' : new_comment, 
        'comment_form' : comment_form,
        'similar_posts': similar_posts,
        })

class PostListView(ListView) :
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blogsite/post/list.html'
    
#Handling forms in views

def post_share( request, post_id ) :
    #Retrieve post by id
    post = get_object_or_404( Post, id = post_id, status = 'published')
    sent = False
    if request.method == 'POST' :
        #Form was submitted
        form = EmailPostForm( request.POST )
        if form.is_valid() :

            #Form fields passed validation
            cd = form.cleaned_data
            # ...send email
            post_url = request.build_absolute_uri( post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail( subject, message, 'christian.85@live.fr', [cd['to']] )
            sent = True
            
            
    else :
        form = EmailPostForm()
        
    return render( request, 'blogsite/post/share.html', {'post' : post, 'form' : form, 'sent' : sent})

#Handling ModelForms in views


        
    
