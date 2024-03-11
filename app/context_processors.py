from .models import Empresa

def add_empresa_to_context(request):
    return {'empresa': Empresa.objects.first(), 'debug_var': 'Debug Variable'}