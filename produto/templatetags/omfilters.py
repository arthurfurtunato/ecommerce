from atexit import register
from django.template import Library
from utils import utils

register = Library()

@register.filter
def formata_preco(val):
    return utils.formatado_preco(val)