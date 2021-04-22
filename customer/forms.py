from django.forms import ModelForm, TextInput 
from cashier.models import Address
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'customer': TextInput(attrs={"readonly":"true", "class":"invisible"}),
            'street_address':TextInput(attrs={"placeholder":"Unit 54, Tower 3, 123 Sesame Street"}),
            'city':TextInput(attrs={"placeholder":"Quezon City"}),
            'home_phone':TextInput(attrs={"placeholder":"8 digit landline (ex. 87241234)", "minlength":8, "maxlength":8}),
            'barangay':TextInput(attrs={"placeholder":"Barangay Valencia"}),
            'zip_code':TextInput(attrs={"placeholder":"1100", "minlength":4})
        }

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField(max_length=254)
    mobile_phone = forms.RegexField(label="Mobile Phone (09xxxxxxxxx)", regex=r'^[0-9]{11}$', error_messages={'invalid': "Please enter a valid phone number format: 09xxxxxxxxx"})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','mobile_phone')

class ImageUploadForm(forms.Form):
    image = forms.ImageField()