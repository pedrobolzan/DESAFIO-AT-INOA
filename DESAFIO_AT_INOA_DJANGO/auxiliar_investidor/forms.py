from django import forms
from .models import Ativo, TunelParametro

class FormAtivo(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = ['nome', 'codigo']

class ParametroTunelForm(forms.ModelForm):
    class Meta:
        model = TunelParametro
        fields = ['limite_inferior', 'limite_superior', 'periodicidade', 'email']