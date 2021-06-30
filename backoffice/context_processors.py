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


def bot_user_list_counter(request):
    department_amounts = None
    if request.user.is_anonymous == False:
        company = request.user.company
        department = models.NewStaff.objects.filter(company=company)
        department_amounts = department.count()
    return {
        'bot_user_list_counter': department_amounts
    }


def staff_gender_statistic(request):
    male = None
    female = None
    if request.user.is_anonymous == False and not request.user.is_superuser == True:
        company =request.user.company
        male = models.Staff.objects.filter(company=company, gender='male')
        female = models.Staff.objects.filter(company=company, gender='female')

        male = male.count()
        female = female.count()
        staff_amount = request.user.company.amount_of_staff
        width_male = int((100*male)/staff_amount)
        width_female = int((100*female)/staff_amount)
        return {
            "male_count": male,
            "female_count": female,
            "company_staff_count": staff_amount,
            "width_male": width_male,
            "width_female": width_female,
        }
    return {
        "male_count": '',
        "female_count": '',
        "company_staff_count": '',
        "width_male": '',
        "width_female": '',
    }
