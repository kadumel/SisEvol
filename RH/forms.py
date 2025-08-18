from django import forms
from django.forms.models import inlineformset_factory
from .models import Funcionario, Vaga, Evento, TipoEvento


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'


class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = '__all__'


class TipoEventoForm(forms.ModelForm):
    class Meta:
        model = TipoEvento
        fields = ['tipo_evento']
        widgets = {
            'tipo_evento': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '40'})
        }


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['tipo', 'descricao', 'Obs', 'vagas', 'empresa']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'Obs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': '250', 'name': 'Obs'}),
            'vagas': forms.NumberInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'form-select'})
        } 