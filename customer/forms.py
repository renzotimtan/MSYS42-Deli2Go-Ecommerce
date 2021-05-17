from django.forms import ModelForm, TextInput 
from cashier.models import Address
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddressForm(ModelForm):
    city = forms.RegexField(widget=TextInput(attrs={"placeholder":"Quezon City"}), regex=r'^[ a-zA-Z0-9]+$', error_messages={'invalid': "Please enter a valid city (no special characters)"})
    barangay = forms.RegexField(widget=TextInput(attrs={"placeholder":"Barangay Valencia"}), regex=r'^[ a-zA-Z0-9]+$', error_messages={'invalid': "Please enter a valid barangay (no special characters)"})
    home_phone = forms.RegexField(widget=TextInput(attrs={"placeholder":"8 digit landline (ex. 87241234)", "minlength":8, "maxlength":8}), regex=r'^[0-9]{8}$', error_messages={'invalid': "Please enter a valid phone number format: xxxxxxxx"}, required=False)
    zip_code = forms.RegexField(widget=TextInput(attrs={"placeholder":"1100", "minlength":4, "maxlength":4}), regex=r'^[0-9]{4}$', error_messages={'invalid': "Please enter a valid zip code: xxxx"})

    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'customer': TextInput(attrs={"readonly":"true", "class":"invisible"}),
            'street_address':TextInput(attrs={"placeholder":"Unit 54, Tower 3, 123 Sesame Street"}),
        }

class RegisterForm(UserCreationForm):
    first_name =  forms.RegexField(label="First Name:", regex=r'^[a-zA-Z]+$', error_messages={'invalid': "Please enter a valid first name (no numbers or special characters)"})
    last_name = forms.RegexField(label="Last Name:", regex=r'^[a-zA-Z]+$', error_messages={'invalid': "Please enter a valid last name (no numbers or special characters)"})
    email = forms.EmailField(max_length=254)
    mobile_phone = forms.RegexField(label="Mobile Phone (09xxxxxxxxx)", regex=r'^[0-9]{11}$', error_messages={'invalid': "Please enter a valid phone number format: 09xxxxxxxxx"})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','mobile_phone')

class ImageUploadForm(forms.Form):
    image = forms.ImageField()