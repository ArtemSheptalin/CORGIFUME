from django.contrib.auth.forms import forms, UserCreationForm
from .models import NewUser
from django.utils.translation import gettext_lazy as _
from .models import Profile


class NewUserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'registrationFormDes', 'required': 'true', 'placeholder': 'Придумайте пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'registrationFormDes', 'required': 'true', 'placeholder': 'Повторите ваш пароль'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': '_req form-ent__input', 'placeholder': 'Введите ваше имя'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': '_req form-ent__input', 'placeholder': 'Номер телефона'}))

    class Meta:
        model = NewUser
        fields = [
            'phone_number', 
            'first_name', 
            'password1', 
            'password2'
        ]


class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))
    email_field = forms.EmailField()

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'city',
            'room',
            'index',
            'house',
            'corp',
            'street',
        ]


class ProfileChangeForm(forms.ModelForm):
    email_field = forms.EmailField(max_length=50)
    
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'city',
            'room',
            'index',
            'house',
            'corp',
            'street',
        ]



    


        




