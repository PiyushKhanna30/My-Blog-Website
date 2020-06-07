from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('<int:post_id>/<int:year>/<int:month>/<int:day>/<slug:slug>/',views.post_detail,name='post_detail'),
	path('<int:post_id>/share/',views.post_share, name='post_share'),



	path('add-post/',views.add_post, name='add_post'),
	path('my-posts/',views.my_post, name='my_post'),
	path('edit-post/<int:post_id>/',views.edit_post, name='edit_post'),
	path('edit-comment/<int:post_id>/<int:comment_id>/<username>',views.delete_comment, name='delete_comment'),
	path('view-my-post/<int:post_id>/',views.view_my_post, name='view_my_post'),
	path('update-profile/',views.update_profile, name='update_profile'),
	path('my-profile/',views.my_profile, name='my_profile'),


	path('delete-comment/<int:post_id>/<int:comment_id>/',views.delete_comment_nonuser,name='delete_comment_nonuser'),
	
	path('user-details/<username>/',views.user_details, name='user_details'),

	path('search-post/',views.search, name='search'),

]