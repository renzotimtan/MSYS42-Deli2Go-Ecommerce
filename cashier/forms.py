from django.forms import ModelForm, Textarea, FileInput, NumberInput
from .models import Item, Order


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'description': Textarea(attrs={'rows': 20}),
            'image': FileInput(attrs={'id': 'files', 'onchange': 'previewImage(event)'}),
            'price': NumberInput(attrs={'min': "0", 'step': '0.01'})
        }
