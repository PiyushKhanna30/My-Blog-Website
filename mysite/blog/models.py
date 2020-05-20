from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
	STATUS_CHOICES = (('draft', 'Draft'),('published', 'Published'),)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250)
	author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
	body = models.TextField()
	publish = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
	
	def __str__(self):
		return self.title
	class Meta:
		verbose_name="Post"
		verbose_name_plural="Posts"
	def get_absolute_url(self):
		return reverse('blog:post_detail',args=[self.id,self.publish.year,self.publish.month,self.publish.day,self.slug])

class Comment(models.Model):
	post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	
	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)
