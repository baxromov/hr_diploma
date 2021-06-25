from django import template

register = template.Library()


@register.filter
def fill_fields(form, model_instance):

    f = form.__class__(instance=model_instance, auto_id=f'%s_{ model_instance.id }_instance_field')

    return f
