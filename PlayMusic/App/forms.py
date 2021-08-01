from App.models import Songs,Movie,User,Rolereq
from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm

class SongsForm(forms.ModelForm):
	class Meta:
		model=Songs
		fields=['moviename','songname','song']
		widgets={
		'moviename':forms.TextInput(attrs={
			'class':"form-control my-2",
			'placeholder':"Enter Movie Name",
			}),
		'songname':forms.TextInput(attrs={
			'class':"form-control my-2",
			'placeholder':'Enter Song Name',
			}),
		'song':forms.FileInput(attrs={
			'class':"form-control my-2",
			'placeholder':"Input Song",
			}),
		}


class MoviesForm(forms.ModelForm):
	class Meta:
		model=Movie
		fields=['moviename','album']
		widgets={
		'moviename':forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Movie name",
			}),
		'album':forms.FileInput(attrs={
			'class':"form-control my-2",
			'placeholder':"Input Image",
			}),
		}


class UsgForm(UserCreationForm):
	password1=forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control my-2",
		"placeholder":"Enter Password",
		}))
	password2=forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control my-2",
		"placeholder":"Confirm Password",
		}))
	class Meta:
		model=User
		fields=['username']
		widgets={
		"username":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter User Name",
			}),

		}

class Rltype(forms.ModelForm):
	class Meta:
		model=Rolereq
		fields=['uname','rltype']
		widgets={
		"uname":forms.TextInput(attrs={
			"class":"form-control my-2",
			"readonly":True,

			}),
		"rltype":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		}

class Rlupd(forms.ModelForm):
	class Meta:
		model=User
		fields=['username','role']
		widgets={
		"username":forms.TextInput(attrs={
			"class":"form-control my-2",
			"readonly":True,
			}),
		"role":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		}


class Pfupd(forms.ModelForm):
	class Meta:
		model=User
		fields=['username','first_name','last_name','email','age','mobilenumber','uimg']
		widgets={
		"uimg":forms.FileInput(attrs={
			"class":"form-control my-2",
			"null":True,
			"blank":True,
			"required":False,
			}),
		"username":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter User Name",
			"blank":True,
			"required":False,
			}),
		"first_name":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter First Name",
			"null":True,
			"blank":True,
			"required":False,
			}),
		"last_name":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Last Name",
			"null":True,
			"blank":True,
			"required":False,
			}),
		"email":forms.EmailInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Email",
			"null":True,
			"blank":True,
			"required":False,
			}),
		"age":forms.NumberInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Age",
			"null":True,
			"blank":True,
			"required":False,
			}),
		"mobilenumber":forms.NumberInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Mobile Number",
			"null":True,
			"blank":True,
			"required":False,
			}),
		# "role":forms.NumberInput(attrs={
		# 	"class":"form-control my-2",
		# 	"readonly":True,
		# 	"required":False,
		# 	}),
		# "is_staff":forms.NumberInput(attrs={
		# 	"class":"form-control my-2",
		# 	"readonly":True,
		# 	"required":False,
		# 	}),
		# "is_active":forms.NumberInput(attrs={
		# 	"class":"form-control my-2",
		# 	"readonly":True,
		# 	"required":False,
		# 	}),
		# "is_superuser":forms.NumberInput(attrs={
		# 	"class":"form-control my-2",
		# 	"readonly":True,
		# 	"required":False,
		# 	}),
		# "date_joined":forms.DateTimeInput(attrs={
		# 	"class":"form-control my-2",
		# 	"readonly":True,
		# 	"required":False,
		# 	}),
		# "last_login":forms.DateTimeInput(attrs={
		# 	"class":"form-control my-2",
		# 	"readonly":True,
		# 	"null":True,
		# 	"blank":True,
		# 	"required":False,
		# 	}),

		}

class Chgepwd(PasswordChangeForm):
	old_password=forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control my-2",
		"placeholder":"Enter Old Password",
		}))
	new_password1=forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control my-2",
		"placeholder":"Enter new Password",
		}))
	new_password2=forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control my-2",
		"placeholder":"Confirm new Password",
		}))

	class Meta:
		model=User
		fields=['old_password','new_password1','new_password2']