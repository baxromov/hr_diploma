from app import models


def staff_amount(request):
    amount_staff = None
    if request.user.is_anonymous == False:
        company = request.user.company
        staff = models.Staff.objects.filter(company=company)
        amount_staff = staff.count()
    return {"amount_staff": amount_staff}


def position_amount(request):
    position_amounts = None
    if request.user.is_anonymous == False:
        company = request.user.company
        position = models.Position.objects.filter(company=company)
        position_amounts = position.count()
    return {
        'position_amounts': position_amounts
    }


def department_amount(request):
    department_amounts = None
    if request.user.is_anonymous == False:
        company = request.user.company
        department = models.Department.objects.filter(company=company)
        department_amounts = department.count()
    return {
        'department_amounts': department_amounts
    }
