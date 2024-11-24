from django import template
import json

register = template.Library()



@register.filter
def clean_array(value):
    value = json.dumps(value)
    value = value.replace("[","")
    value = value.replace("]","")
    return value.replace("-1","X")