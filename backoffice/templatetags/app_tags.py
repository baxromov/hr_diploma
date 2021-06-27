from django import template
from app import models
register = template.Library()


@register.filter
def fill_fields(form, model_instance):

    f = form.__class__(instance=model_instance, auto_id=f'%s_{ model_instance.id }_instance_field')

    return f

@register.filter
def late_delta(action_time, user):
    import datetime
    today_name = datetime.datetime.today().strftime('%A')
    company_schedule = models.CompanySchedule.objects.filter(company=user.company, day__exact=today_name.lower()).first()
    coming_time = datetime.datetime.strptime(action_time, "%H:%M")
    schedule = datetime.datetime.strptime(str(company_schedule.start_work), "%H:%M:%S")
    # return coming_time - schedule

    if coming_time > schedule:
        # late
        return coming_time - schedule
    elif coming_time < schedule:
        return schedule - coming_time


@register.filter
def late_delta_bool(action_time, user):
    import datetime
    today_name = datetime.datetime.today().strftime('%A')
    company_schedule = models.CompanySchedule.objects.filter(company=user.company, day__exact=today_name.lower()).first()
    coming_time = datetime.datetime.strptime(action_time, "%H:%M")
    schedule = datetime.datetime.strptime(str(company_schedule.start_work), "%H:%M:%S")
    if coming_time > schedule:
        return True
    elif coming_time < schedule:
        return False

