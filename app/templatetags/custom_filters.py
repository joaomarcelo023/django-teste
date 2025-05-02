from django import template

register = template.Library()

UNIT_SYMBOLS = {
    "M2": "m²",
    "m2": "m²",
    "CM2": "cm²",
    "cm2": "cm²",
    "M3": "m³",
    "m3": "m³",
    "CM3": "cm³",
    "cm3": "cm³",
    "KG": "kg",
    "G": "g",
    "MM": "mm",
    "UN": "un",
    "PC": "pc",
    "MT": "mt",
}

@register.filter
def format_unit(value):
    """Convert unit abbreviations to symbols."""
    return UNIT_SYMBOLS.get(value.upper(), value)

@register.filter
def gt(value, arg):
    return value > arg

@register.filter
def lt(value, arg):
    return value < arg

@register.filter
def comma_point(value):
    return value.replace(".", ",")

@register.filter
def prod(value, arg):
    return round((float(value) * float(arg)), 2)

@register.filter
def orGet(value, arg):
    if value:
        return value
    else:
        return arg

@register.filter
def getByTitulo(value, arg):
    return value[arg]