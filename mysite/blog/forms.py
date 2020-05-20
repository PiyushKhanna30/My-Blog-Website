from django import forms
from .models import Comment,Post,User

class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=25,widget=forms.HiddenInput)
	email = forms.EmailField(widget=forms.HiddenInput)
	to = forms.EmailField()
	comments = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name','email','body')
		widgets = {
                   'name':forms.HiddenInput(),
                   'email':forms.HiddenInput(), 
		        }

class PostForm(forms.ModelForm):
	STATUS_CHOICES = (('draft', 'Draft'),('published', 'Published'),)
	status=forms.ChoiceField(choices=STATUS_CHOICES)
	class Meta:
		model=Post
		fields=('title','body','status')
class EditPostForm(forms.ModelForm):
	STATUS_CHOICES = (('draft', 'Draft'),('published', 'Published'),)
	status=forms.ChoiceField(choices=STATUS_CHOICES)
	class Meta:
		model=Post
		fields=('title','body','status')
		widgets = {
          'body': forms.Textarea(attrs={'rows':20, 'cols':70}),
        }
class UserForm(forms.ModelForm):
	class Meta:
		model=User
		fields=('first_name','last_name',)