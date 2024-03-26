from django import forms
from.models import Pedido_order, Cliente, Endereco
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
    senha = forms.CharField(widget = forms.PasswordInput (attrs={'placeholder' : 'Sua Senha', 'class' : "form-control", 'style': 'width: 300px;display: flex;'}))
    email = forms.CharField(widget = forms.EmailInput (attrs={'placeholder' : 'Seu Email', 'class' : "form-control", 'style': 'width: 300px;display: flex;'}))

    class Meta:
        model = Cliente
        fields = ["email","senha","nome","sobrenome","cpf","telefone"]

        widgets = {

            'nome': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Nome'
            }),
            'sobrenome': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Sobrenome'
            }),
            'cpf': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'CPF'
            }),
            'telefone': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Telefone'
            }),

        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Este cliente já existe no banco de dados")
        return cleaned_data

class ClienteEntrarForms(forms.Form):
    email = forms.CharField(widget=forms.TextInput(
            attrs={'placeholder': 'Email', 'class': "form-control", 'style': 'width: 300px;display: flex;'}))
    senha = forms.CharField(widget=forms.PasswordInput(
            attrs={'placeholder': 'Sua Senha', 'class': "form-control", 'style': 'width: 300px;display: flex;'}))

class EnderecoRegistrarForms(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ["titulo","cep","estado","cidade","bairro","rua","numero","complemento"]

        widgets = {

            'titulo': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Nome'
            }),
            'cep': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Sobrenome'
            }),
            'estado': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'estado'
            }),
            'cidade': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'CPF'
            }),
            'bairro': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Telefone'
            }),
            'rua': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Telefone'
            }),
            'numero': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Telefone'
            }),
            'complemento': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Telefone'
            }),

        }
