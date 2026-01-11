from django import forms
from .models import ChatMessage

OFFENSIVE_WORDS = ['banned', 'offensive', 'spam', 'tonto', 'idiota'] 

class ChatMessageForm(forms.ModelForm):
    """
    Formulari per escriure missatges.
    """
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Escriu un missatge...',
                'maxlength': '500' # Màxim 500 caràcters
            })
        }

    def clean_message(self):
        """
        Comprova que el missatge estigui bé:
        - No buit
        - No massa llarg
        - Sense insults
        """
        message = self.cleaned_data.get('message', '').strip()
        
        # Si està buit, error
        if not message:
            raise forms.ValidationError("El missatge no pot estar buit.")
        
        # Si és massa llarg, error
        if len(message) > 500:
             raise forms.ValidationError("El missatge és massa llarg.")

        # Si té insults, error
        lower_msg = message.lower()
        for word in OFFENSIVE_WORDS:
            if word in lower_msg:
                raise forms.ValidationError("El missatge conté paraules ofensives.")
        
        return message
