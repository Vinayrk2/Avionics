from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class UserSignUpForm(UserCreationForm):
    
	class Meta:
		model  = CustomUser
		fields = ["username","first_name","last_name","password1","email","phone_number","address","image"]

	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args,**kwargs)

		for fieldname in ['username', 'password1', 'password2','email',"phone_number","address","image","first_name","last_name"]:
			self.fields[fieldname].help_text = None
			self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
		if 'usable_password' in self.fields:
			del self.fields['usable_password']
   
class UserLoginForm(AuthenticationForm):
	
	class Meta:
		model = CustomUser
	
	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)
  
		for fieldname in ['username', 'password']:
			self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
		