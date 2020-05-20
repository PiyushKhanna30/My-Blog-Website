from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254,required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2' )

    def clean_email(self):
    	email=self.cleaned_data['email'].lower()
    	r=User.objects.filter(email=email)
    	if r.count():
    		raise ValidationError('Email already exists.')
    	return email
	# def clean_email(self):
	# 	email = self.cleaned_data['email'].lower()
	# 	r = User.objects.filter(email=email)
	# 	if r.count():
	# 		raise  ValidationError("Email already exists")
	# 	return email

'''

class UserRegistrationForm(forms.ModelForm):
	email = forms.EmailField(max_length=254,required=True)
	password = forms.CharField(label='Password',widget=forms.PasswordInput)
	password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('username', 'first_name','last_name','email')
	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Passwords don\'t match.')
		return cd['password2']
	def clean_email(self):
		cd = self.cleaned_data
		if User.objects.get(email=cd['email']).exists:
			raise ValidationError("Email exists.")
		return cd['email']

def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email
'''