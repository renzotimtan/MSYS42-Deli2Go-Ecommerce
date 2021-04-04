from django.forms import ModelForm, TextInput 
from cashier.models import Address
from django.core.exceptions import ValidationError

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'customer': TextInput(attrs={"readonly":"true", "class":"invisible"}),
        }
    