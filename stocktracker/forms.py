from django import forms

class CreateAccountForm(forms.Form):
	username = forms.CharField(min_length="5", max_length="30")
	password1 = forms.CharField(min_length="5", max_length="30")
	password1.widget = forms.PasswordInput()
	password2 = forms.CharField(min_length="5", max_length="30")
	password2.widget = forms.PasswordInput()
	email = forms.EmailField(required=False)
	first_name = forms.CharField(max_length="30")
	last_name = forms.CharField(max_length="30")

class CreateLoginForm(forms.Form):
	username = forms.CharField(min_length="5", max_length="30")
	password = forms.CharField(min_length="5", max_length="30")
	password.widget = forms.PasswordInput()