from django import forms
from models import User, Messageboard_Message

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "image",
        ]
class Messageboard_MessageForm(forms.ModelForm):
    class Meta:
        model = Messageboard_Message
        fields = [
        "title",
        "message",
        "image",
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Title'}),
            'message': forms.Textarea(attrs={'placeholder':'Message'}),
        }
