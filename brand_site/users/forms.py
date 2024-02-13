from django.contrib.auth.forms import forms, UserCreationForm
from .models import NewUser
from django.utils.translation import gettext_lazy as _
from .models import Profile


class NewUserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'registrationFormDes', 'required': 'true', 'placeholder': 'Придумайте пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'registrationFormDes', 'required': 'true', 'placeholder': 'Повторите ваш пароль'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': '_req form-ent__input', 'placeholder': 'Введите ваше имя'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': '_req form-ent__input', 'placeholder': 'Номер телефона'}))
    email_for_reset = forms.CharField(widget=forms.TextInput(attrs={'class': '_req form-ent__input', 'placeholder': 'E-mail адрес'}))
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'class': '_req form-ent__input', 'placeholder': 'Дата рождения', 'id': 'birthId'}))

    class Meta:
        model = NewUser
        fields = [
            'phone_number', 
            'first_name', 
            'password1', 
            'password2',
            'email_for_reset'
        ]


class ProfileForm(forms.ModelForm):
    first_name = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    last_name = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    date_of_birth = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    city = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Номер телефона', 'readonly': 'readonly'}))
    email_field = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    room = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    index = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    house = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    corp = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    street = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Profile
        fields = ()


class ProfileChangeForm(forms.ModelForm):
    email_field = forms.EmailField(max_length=50)
    
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'city',
            'room',
            'index',
            'house',
            'corp',
            'street',
        ]



    


        




