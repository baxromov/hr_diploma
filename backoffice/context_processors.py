from app import models


def staff_amount(request):
    company = request.user.company
    staff = models.Staff.objects.filter(company=company)
    amount_staff = staff.count()
    return {"amount_staff": amount_staff}


def position_amount(request):
    company = request.user.company
    position = models.Position.objects.filter(company=company)
    position_amounts = position.count()
    return {
        'position_amounts': position_amounts
    }


def department_amount(request):
    company = request.user.company
    department = models.Department.objects.filter(company=company)
    department_amounts = department.count()
    return {
        'department_amounts': department_amounts
    }
