from django.shortcuts import render,get_object_or_404,redirect
# Create your views here.
from .models import Post,User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import EmailPostForm
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm,PostForm,EditPostForm,UserForm
from django.template.defaultfilters import slugify
from django.urls import reverse


@login_required
def post_list(request):
	posts = Post.objects.filter(status='published')
	
	paginator = Paginator(posts, 5)
	#2 get page number
	page = request.GET.get('page')
	# bel0w we put page n0 and get c0rresp0nding items 0n that page
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
	# If page is not an integer deliver the first page
		posts = paginator.page(1)
	except EmptyPage:
	# If page is out of range deliver last page of results
		posts = paginator.page(paginator.num_pages)		
	return render(request,'list.html',{'posts': posts})

@login_required
def post_detail(request,post_id, year, month, day, slug):
	post = get_object_or_404(Post, pk=post_id,slug=slug,status='published',publish__year=year,publish__month=month,publish__day=day)
	# List of active comments for this post 
# We specify the name of the reverse relationship, from User to Post, with
# the related_name attribute. This will allow us to access related objects easily
	comments=post.comments.filter(active=True).order_by('-created')
	# or ^| comments = Comment.objects.filter(active=True,post=post)
	new_comment = None
	loggedin_user = request.user
	data={'name':loggedin_user.username,'email':loggedin_user.email}
	if request.method == 'POST':
		# A comment was posted
		comment_form = CommentForm(request.POST,initial=data)
		if comment_form.is_valid():
			cd = comment_form.cleaned_data
			# Create Comment object but don't save to database yet
			# new_comment = Comment(name=post.author.username,email=post.author.email,body=cd['body'])
			new_comment=comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.post = post
			# Save the comment to the database
			new_comment.save()
			comment_form = CommentForm(initial=data)
			return redirect(request.build_absolute_uri(post.get_absolute_url()))
			# return render(request,'detail.html',{'post': post,'comments': comments,'new_comment': new_comment,'comment_form': comment_form})

	else:
		comment_form = CommentForm(initial=data)
		#paginating comments
	paginator = Paginator(comments, 5)
	page = request.GET.get('page')
	try:
		comments = paginator.page(page)
	except PageNotAnInteger:
		comments = paginator.page(1)
	except EmptyPage:
		comments = paginator.page(paginator.num_pages)
	return render(request,'detail.html',{'post': post,'comments': comments,'new_comment': new_comment,'comment_form': comment_form})

@login_required
def post_share(request, post_id):
	# Retrieve post by id
	post = get_object_or_404(Post, pk=post_id, status='published')
	sent = False
	loggedin_user = request.user
	data={'name':loggedin_user.username,'email':loggedin_user.email}
	if request.method == 'POST':
	# Form was submitted
		form = EmailPostForm(request.POST,initial=data)
		if form.is_valid():
			# Form fields passed validation
			cd = form.cleaned_data
			# send email
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
			send_mail(subject, message, 'pythonadvance@gmail.com',[cd['to']])
			sent = True

	else:
		form = EmailPostForm(initial=data)
	return render(request, 'share.html', {'post': post,'form': form,'sent': sent})

@login_required
def add_post(request):
	loggedin_user = request.user
	if request.method=='POST':
		form=PostForm(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			post_object=form.save(commit=False)
			post_object.author=loggedin_user
			post_object.slug=slugify(cd['title'])
			post_object.save()
			return redirect(reverse('blog:my_post'))
	else:
		form=PostForm()
	return render(request,'add_post.html',{'form':form})

@login_required
def my_post(request):
	loggedin_user = request.user
	posts = Post.objects.filter(author=loggedin_user)
	paginator = Paginator(posts, 5)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request,'mylist.html',{'posts': posts})

@login_required
def edit_post(request,post_id):
	loggedin_user = request.user
	post = get_object_or_404(Post,pk=post_id,author=loggedin_user)
	comments=post.comments.filter(active=True).order_by('-created')
	data={'title':post.title,'body':post.body,'status':post.status}
	if request.method=='POST':
		form=EditPostForm(request.POST,instance=post)
		if form.is_valid():
			# cd=form.cleaned_data
			form.save()
			return redirect(reverse('blog:view_my_post',args=[post_id]))
	else:
		form=EditPostForm(initial=data,instance=post)
	return render(request,'edit_post.html',{'form':form,'post':post,'comments':comments})

@login_required
def delete_comment(request,post_id,comment_id,username):
	post=get_object_or_404(Post,pk=post_id,author=request.user)
	comment = get_object_or_404(Comment,pk=comment_id)
	comment.active=False;
	comment.save()
	return redirect(reverse('blog:edit_post',args=[post_id]))

@login_required
def delete_comment_nonuser(request,post_id,comment_id):
	comment = get_object_or_404(Comment,pk=comment_id,name=request.user.username)
	comment.active=False;
	comment.save()
	post=Post.objects.get(id=post_id)
	return redirect(reverse('blog:post_detail',args=[post_id, post.publish.year, post.publish.month,post.publish.day,post.slug]))

	# request,post_id, year, month, day, slug
@login_required
def view_my_post(request,post_id):
	loggedin_user = request.user
	post = get_object_or_404(Post,pk=post_id,author=loggedin_user)
	comments=post.comments.filter(active=True).order_by('-created')
	paginator = Paginator(comments, 5)
	page = request.GET.get('page')
	try:
		comments = paginator.page(page)
	except PageNotAnInteger:
		comments = paginator.page(1)
	except EmptyPage:
		comments = paginator.page(paginator.num_pages)
	return render(request,'view_my_post.html',{'post': post,'comments': comments})

@login_required
def update_profile(request):
	loggedin_user = request.user
	if request.method=='POST':
		form=UserForm(request.POST,initial={'first_name':loggedin_user.first_name,'last_name':loggedin_user.last_name,},instance=loggedin_user)
		if form.is_valid():
			form.save()
			return redirect(reverse('blog:post_list'))
	else:
		form=UserForm(initial={'first_name':loggedin_user.first_name,'last_name':loggedin_user.last_name,},instance=loggedin_user)
	return render(request,'update_profile.html',{'user':loggedin_user,'form':form})

@login_required
def my_profile(request):
	loggedin_user = request.user
	post=Post.objects.filter(author=loggedin_user)
	return render(request,'my_profile.html',{'user':loggedin_user,'posts':post})

@login_required
def user_details(request,username):
	user=User.objects.get(username=username)
	post=Post.objects.filter(author=user,status='published')
	return render(request,'user_details.html',{'user':user,'posts':post})