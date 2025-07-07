from django import forms
from .models import PedidoOrder, Cliente, Endereco, FotosProduto
from django.db.models import fields
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, EmailInput
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from validate_docbr import CPF, CNPJ

# TODO: Acho que esse checar_PedidoForms não é utilizado
# class Checar_PedidoForms(forms.ModelForm):
#     class Meta:
#         model = PedidoOrder
#         fields = ['ordenado_por',"endereco_envio","telefone"]

#         labels = {
#             'ordenado_por': 'Nome do recebedor',
#             'endereco_envio': 'Endereço de envio',
#             'telefone': 'Telefone'
#         }
#         widgets = {
#             'ordenado_por': TextInput(attrs={
#                 'class': 'form-control',
#                 'style': 'max-width: 100%;',
#                 'placeholder': 'Nome Completo'
#             }),
#             'endereco_envio': TextInput(attrs={
#                 'class': 'form-control',
#                 'style': 'max-width: 100%;',
#                 'placeholder': 'Endereço de envio'
#             }),
#             'telefone': TextInput(attrs={
#                 'class': 'form-control',
#                 'style': 'max-width: 100%;',
#                 'placeholder': 'Telefone'
#             }),
#         }

class ClienteRegistrarForms(forms.ModelForm):
    senha = forms.CharField(widget = forms.PasswordInput (attrs={
        'placeholder': 'Sua Senha',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;'
    }))
    email = forms.CharField(widget = forms.EmailInput (attrs={
        'placeholder': 'Seu Email',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;'
    }))


    telefone_validator = RegexValidator(regex=r'^\(\d{2}\)\s\d{5}-\d{3,4}_?$',message="O número de telefone deve conter DDD mais 8 ou 9 dígitos numéricos.")
    cpf_validator = RegexValidator(regex=r'^\d{11,14}$',message="O número de CPF ou CNPJ deve conter 11 ou 14 dígitos numéricos.")
    
    telefone = forms.CharField(validators=[telefone_validator], label="Telefone", widget=TextInput(attrs={
        'class': "form-control phone-number",
        'style': 'max-width: 100%;',
        'inputmode': 'numeric',
        'placeholder': 'Telefone (apenas números)',
        # 'placeholder': '(__) _____-____'
    })) #, max_length = 15)

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
                'class': 'form-control',
                'style': 'max-width: 100%;',
                'placeholder': 'Nome'
            }),
            'sobrenome': TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 100%;',
                'placeholder': 'Sobrenome'
            }),

        }

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Este cliente já existe no banco de dados")
        
        cpf_cnpj = cleaned_data.get("cpf_ou_cnpj")
        cpf = CPF()
        cnpj = CNPJ()
        if (not cpf.validate(cpf_cnpj)) and (not cnpj.validate(cpf_cnpj)):
            raise forms.ValidationError("CPF ou CNPJ invalido")

        return cleaned_data

class ClienteEntrarForms(forms.Form):
    email = forms.CharField(label="E-mail", widget=forms.TextInput(attrs={
        'placeholder': 'E-mail',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;'
    }))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Senha',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;'
    }))

class EnderecoRegistrarForms(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ["titulo","cep","estado","cidade","bairro","rua","numero","complemento"]

        widgets = {
            'titulo': TextInput(attrs={
                'class': 'form-control',
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
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Bairro'
            }),
            'rua': TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Rua'
            }),
            'numero': TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'inputmode': 'numeric',
                'placeholder': 'Número'
            }),
            'complemento': TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Complemento'
            }),

        }

class ClienteEditarEndereco(forms.Form):
    titulo = forms.CharField(widget=TextInput(attrs={
        'id': 'titulo',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;',
        'placeholder': 'Título (opcional)'
    }), required=False)

    cep = forms.CharField(widget=TextInput(attrs={
        'id': 'cep',
        'class': "form-control cep-input",
        'style': 'width: 100%; display: flex;',
        'inputmode': 'numeric',
        'placeholder': 'CEP'
    }))

    estado = forms.CharField(widget=TextInput(attrs={
        'id': 'estado',
        'class': "form-control estado-input",
        'style': 'width: 100%; display: flex; pointer-events: none;',
        'readonly': 'true',
        'placeholder': 'Estado'
    }))

    cidade = forms.CharField(widget=TextInput(attrs={
        'id': 'cidade',
        'class': "form-control cidade-input",
        'style': 'width: 100%; display: flex; pointer-events: none;',
        'readonly': 'true',
        'placeholder': 'Cidade'
    }))
    
    bairro = forms.CharField(widget=TextInput(attrs={
        'id': 'bairro',
        'class': 'form-control',
        'style': 'width: 100%; display: flex; pointer-events: none;',
        'readonly': 'true',
        'placeholder': 'Bairro'
    }))
    
    rua = forms.CharField(widget=TextInput(attrs={
        'id': 'rua',
        'class': 'form-control',
        'style': 'width: 100%; display: flex; pointer-events: none;',
        'readonly': 'true',
        'placeholder': 'Rua'
    }))
    
    numero = forms.CharField(widget=TextInput(attrs={
        'id': 'numero',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;',
        'inputmode': 'numeric',
        'placeholder': 'Número'
    }))
    
    complemento = forms.CharField(widget=TextInput(attrs={
        'id': 'complemento',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;',
        'placeholder': 'Complemento'
    }), required=False)

class ClienteEditarNome(forms.Form):
    nome = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Nome',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;'
    }))
    sobrenome = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Sobrenome',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;'
    }))

class ClienteEditarEmail(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'E-mail',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;'
    }))
    
class ClienteEditarCPF(forms.Form):
    cpf_validator = RegexValidator(regex=r'^\d{11,14}$',message="O número de CPF ou CNPJ deve conter 11 ou 14 dígitos numéricos.")

    cpf_ou_cnpj = forms.CharField(validators=[cpf_validator],widget=forms.TextInput(attrs={
        'placeholder': 'CPF ou CNPJ (apenas números)',
        'class': 'form-control cpf-cnpj',
        'style': 'width: 100%; display: flex;',
        'inputmode': 'numeric',
    }), max_length = 14)

    def clean(self):
        cleaned_data = super().clean()
        
        cpf_cnpj = cleaned_data.get("cpf_ou_cnpj")
        cpf = CPF()
        cnpj = CNPJ()
        if (not cpf.validate(cpf_cnpj)) and (not cnpj.validate(cpf_cnpj)):
            raise forms.ValidationError("CPF ou CNPJ invalido")

        return cleaned_data
    
class ClienteEditarTelefone(forms.Form):
    telefone_validator = RegexValidator(regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}_?$',message="O número de telefone deve conter DDD mais 8 ou 9 dígitos numéricos.")

    telefone = forms.CharField(validators=[telefone_validator], widget=TextInput(attrs={
        'placeholder': 'Telefone (apenas números)',
        'class': 'form-control phone-number',
        'style': 'width: 100%; display: flex;',
        'inputmode': 'numeric',
        # 'placeholder': '(__) _____-____',
    }), max_length = 15)

class ClienteAlterarSenhaForms(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'E-mail',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;'
    }))
    senha_antiga = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Senha antiga',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;'
    }))
    senha_nova = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Senha nova',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;'
    }))
    repita_a_senha_nova = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita a senha nova',
        'class': 'form-control',
        'style': 'width: 100%; display: flex;'
    }))

class ProdutosImagemExtraForm(forms.ModelForm):
    class Meta:
        model = FotosProduto
        fields = ['image']