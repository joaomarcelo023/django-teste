from django import forms
from .models import Pedido_order, Cliente, Endereco
from django.db.models import fields
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, EmailInput
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

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
    senha = forms.CharField(widget = forms.PasswordInput (attrs={'placeholder' : 'Sua Senha', 'class' : "form-control", 'style': 'width: 100%;display: flex;'}))
    email = forms.CharField(widget = forms.EmailInput (attrs={'placeholder' : 'Seu Email', 'class' : "form-control", 'style': 'width: 100%;display: flex;'}))


    telefone_validator = RegexValidator(regex=r'^\(\d{2}\)\s\d{5}-\d{3,4}_?$',message="O número de telefone deve conter DDD mais 8 ou 9 dígitos numéricos.")
    cpf_validator = RegexValidator(regex=r'^\d{11,14}$',message="O número de CPF ou CNPJ deve conter 11 ou 14 dígitos numéricos.")
    
    telefone = forms.CharField(validators=[telefone_validator], label="Telefone", widget=TextInput(attrs={
        'class': "form-control phone-number",
        'style': 'max-width: 100%;',
        'inputmode': 'numeric',
        'placeholder': 'Telefone (apenas números)',
        # 'placeholder': '(__) _____-____'
    }), max_length = 15)

    cpf_ou_cnpj = forms.CharField(validators=[cpf_validator], label="CPF ou CNPJ", widget=TextInput(attrs={
        'class': "form-control cpf-cnpj",
        'style': 'max-width: 100%;',
        'inputmode': 'numeric',
        'placeholder': 'CPF ou CNPJ (apenas números)'
    }), max_length = 14)

    class Meta:
        model = Cliente
        fields = ["nome","sobrenome","email","senha","cpf_ou_cnpj","telefone"]

        widgets = {

            'nome': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%;',
                'placeholder': 'Nome'
            }),
            'sobrenome': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%;',
                'placeholder': 'Sobrenome'
            }),

        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Este cliente já existe no banco de dados")
        return cleaned_data

class ClienteEntrarForms(forms.Form):
    email = forms.CharField(label="E-mail", widget=forms.TextInput(
            attrs={'placeholder': 'E-mail', 'class': "form-control", 'style': 'width: 100%;display: flex;'}))
    senha = forms.CharField(widget=forms.PasswordInput(
            attrs={'placeholder': 'Senha', 'class': "form-control", 'style': 'width: 100%;display: flex;'}))

class EnderecoRegistrarForms(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ["titulo","cep","estado","cidade","bairro","rua","numero","complemento"]

        widgets = {

            'titulo': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Título (opcional)'
            }),
            'cep': TextInput(attrs={
                'class': "form-control cep-input",
                'style': 'max-width: 300px;',
                'inputmode': 'numeric',
                'placeholder': 'CEP'
            }),
            'estado': TextInput(attrs={
                'class': "form-control estado-input",
                'style': 'max-width: 300px;',
                'placeholder': 'Estado'
            }),
            'cidade': TextInput(attrs={
                'class': "form-control cidade-input",
                'style': 'max-width: 300px;',
                'placeholder': 'Cidade'
            }),
            'bairro': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Bairro'
            }),
            'rua': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Rua'
            }),
            'numero': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'inputmode': 'numeric',
                'placeholder': 'Número'
            }),
            'complemento': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Complemento'
            }),

        }
