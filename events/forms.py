from django import forms
from .models import Event, STATUS_CHOICES, CATEGORY_CHOICES

class EventCreationForm(forms.ModelForm):
    """
    Formulari per a la creació de nous esdeveniments.
    - Defineix quins camps del model Event s'han d'emplenar.
    - Personalitza els widgets (calendari per a dates, àrea de text per a descripcions).
    """
    class Meta:
        model = Event
        fields = ['title','description','category','scheduled_date','thumbnail','max_viewers','tags','status','stream_url']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type':'datetime-local'}), # Selector natiu de data i hora HTML5
            'description': forms.Textarea(), # Àrea de text gran
        }

class EventUpdateForm(forms.ModelForm):
    """
    Formulari per a l'edició d'esdeveniments.
    Similar al de creació, però pot incloure lògica específica si calgués diferenciar-los en el futur.
    Inclou tots els camps editables.
    """
    class Meta:
        model = Event
        fields = ['title','description','category','scheduled_date','thumbnail','max_viewers','tags','status','stream_url']

class EventSearchForm(forms.Form):
    """
    Formulari de cerca i filtratge per al llistat d'esdeveniments.
    No està lligat a cap model (és un form normal), només serveix per processar paràmetres GET.
    Camps:
    - search: Text lliure per cercar per títol.
    - category: Desplegable amb les categories definides al model.
    - status: Desplegable amb els estats definides al model.
    - date_from / date_to: Filtratge per rang de dates.
    """
    search = forms.CharField(required=False, label="Cerca")
    category = forms.ChoiceField(
        choices=[('', 'Totes')] + CATEGORY_CHOICES, 
        required=False,
        label="Categoria"
    )
    status = forms.ChoiceField(
        choices=[('', 'Tots')] + STATUS_CHOICES,
        required=False,
        label="Estat"
    )
    date_from = forms.DateField(required=False, label="Data inici", widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, label="Data fi", widget=forms.DateInput(attrs={'type': 'date'}))
