from django import forms
from.models import Pedido_order, Cliente
from django.db.models import fields
from django.forms import ModelForm, TextInput, EmailInput
from django.contrib.auth.models import User





class Checar_PedidoForms(forms.ModelForm):
    class Meta:
        model = Pedido_order
        fields = ['ordenado_por',"endereco_envio","telefone","email"]

        widgets = {
            'ordenado_por': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'ordenado_por'
            }),
            'endereco_envio': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Endereco de envio'
            }),
            'telefone': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Telefone'
            }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
            }),

        }

class ClienteRegistrarForms(forms.ModelForm):
    usuario = forms.CharField(widget = forms.TextInput (attrs={'placeholder' : 'Usuario', 'class' : "form-control", 'style': 'width: 300px;display: flex;'}))
    senha = forms.CharField(widget = forms.PasswordInput (attrs={'placeholder' : 'Sua Senha', 'class' : "form-control", 'style': 'width: 300px;display: flex;'}))
    email = forms.CharField(widget = forms.EmailInput (attrs={'placeholder' : 'Seu Email', 'class' : "form-control", 'style': 'width: 300px;display: flex;'}))

    class Meta:
        model = Cliente
        fields = ['usuario',"senha","email","nome_completo","endereco"]

        widgets = {

            'nome_completo': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Nome Completo'
            }),
            'endereco': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Endereco'
            }),

        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("usuario")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este cliente já existe no banco de dados")
        return cleaned_data

class ClienteEntrarForms(forms.Form):
    usuario = forms.CharField(widget=forms.TextInput(
            attrs={'placeholder': 'Usuario', 'class': "form-control", 'style': 'width: 300px;display: flex;'}))
    senha = forms.CharField(widget=forms.PasswordInput(
            attrs={'placeholder': 'Sua Senha', 'class': "form-control", 'style': 'width: 300px;display: flex;'}))
