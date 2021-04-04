from django.forms import ModelForm, TextInput 
from cashier.models import Address
from django.core.exceptions import ValidationError

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'customer': TextInput(attrs={"readonly":"true", "class":"invisible"}),
            'street_address':TextInput(attrs={"placeholder":"Unit 54, Tower 3, 123 Sesame Street"}),
            'city':TextInput(attrs={"placeholder":"Quezon City"}),
            'home_phone':TextInput(attrs={"placeholder":"8 digit landline (ex. 87241234)"}),
            'barangay':TextInput(attrs={"placeholder":"Barangay Valencia"}),
            'zip_code':TextInput(attrs={"placeholder":"1100"})
        }
    