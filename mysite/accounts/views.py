from .forms import UserRegistrationForm
from django.urls import reverse
from django.shortcuts import render,get_object_or_404,redirect

def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user=user_form.cleaned_data
			user_form.save()
			return render(request,'registration/register_success.html',{'user':new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request,'registration/register.html',{'user_form': user_form})