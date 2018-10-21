# chat/forms.py
"""
Forms for Chat App - DjangoChat project
"""
from django.forms import ModelForm
from chat.models import Profile


class ProfileForm(ModelForm):
    """
    ProfileForm Class.
    """
    class Meta:
        """
        Meta Class
        """
        model = Profile
        fields = ('first_name', 'last_name', 'email')
