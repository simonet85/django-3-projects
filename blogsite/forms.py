from django import forms
from .models import Comment


class EmailPostForm( forms.Form ) :
    name = forms.CharField( max_length = 25 )
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField( required = False, widget = forms.Textarea )
    
#create forms from models (Django has two base classes to build forms: Form and ModelForm)
class CommentForm( forms.ModelForm ) :
    #To create a form from a model, you just need to indicate which model to use to build the form in the Meta class of the form.
    class Meta :
        model = Comment
        fields = ['name', 'email', 'body']
        
class SearchForm( forms.Form ) :
    query = forms.CharField()
