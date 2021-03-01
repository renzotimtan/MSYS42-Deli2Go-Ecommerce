from django.forms import ModelForm, Textarea, FileInput
from .models import Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'description': Textarea(attrs={'rows': 20}),
            'image': FileInput(attrs={'id': 'files', 'onchange': 'previewImage(event)'})
        }