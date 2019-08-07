from django import template

register = template.Library()

@register.assignment_tag
def hello_world(name):
    value = name.split('/')[-4]
    if value == "institute": return True; return False