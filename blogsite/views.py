from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import EmailPostForm
from django.core.mail import send_mail
 
def post_list( request ) :
    #posts = Post.published.all()
    object_list = Post.published.all()
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
   
    return render( request, 'blogsite/post/list.html',{'page':page, 'posts' : posts} )

def post_detail( request, year, month, day, post ) :
    post = get_object_or_404(Post, slug=post, status = 'published', publish__year = year, publish__month = month, publish__day = day)
    return render( request, 'blogsite/post/detail.html', {'post' : post})

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



        
    
