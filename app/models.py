from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor import fields
from ckeditor_uploader.fields import RichTextUploadingField


def get_directory(instance, filename):
    return 'files/{0}/{1}'.format(f'{instance.first_name} {instance.second_name} {instance.last_name}', filename)


class TypeCompany(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kompaniya turini nomi")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Kompaniya turi"

    def __str__(self):
        return self.name


# class Qurilma(models.Model):
#     name = models.CharField(max_length=100)
#     company = models.ForeignKey('Company', on_delete=models.CASCADE)


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kompaniya nomi")
    phone = models.CharField(max_length=25, null=True, blank=True, verbose_name="Kompaniya telefon raqami")
    type = models.ForeignKey(TypeCompany, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name="Kompaniya turi")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Kompaniya manzili")
    #
    creator = models.CharField(max_length=255, null=True, blank=True, verbose_name="Kompaniya asoschisi")
    text = RichTextUploadingField(null=True, blank=True, verbose_name="Kompaniya haqida qisqacha ma'lumot")
    video = models.FileField(upload_to='company/video/', null=True, blank=True,
                             verbose_name="Kompaniya haqida qisqacha video")
    info = models.TextField(null=True, blank=True, verbose_name="Bot uchun qisqacha ma'lumot")
    logo = models.ImageField(upload_to='company/image/', null=True, blank=True, verbose_name="Kompaniya logotipi")
    amount_of_staff = models.IntegerField(verbose_name="Hodimlar soni", default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'#{self.id}  {self.name}'

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Kompaniya ma'lumotini qo'shish"


class Branch(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Filial")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Filial"

    def __str__(self):
        return self.name


class User(AbstractUser):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Filial")
    company = models.ForeignKey("Company", on_delete=models.CASCADE, null=True, blank=True, verbose_name='Kompaniya')
    is_director = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "HR"

    def save(self, *args, **kwargs):
        if not 'sha256' in self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name="Bo'lim nomi")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Kompaniya')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Bo'limlar"


class Position(models.Model):
    name = models.CharField(max_length=255, verbose_name="Lavozim nomi")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Kompaniya')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Lavozim"


class Promotion(models.Model):
    surcharge = models.BooleanField(default=False, verbose_name="Jarima")
    reward = models.BooleanField(default=False, verbose_name="Mukofot")
    note = models.CharField(max_length=512, null=True, blank=True, verbose_name="Izoh")
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, verbose_name="Xodim")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Xodimlarga jarima mukofot e'lon qilish"

    def __str__(self):
        return f'{self.staff.first_name} {self.staff.second_name} {self.staff.last_name}'


class VacationType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    create_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kompaniya")

    class Meta:
        verbose_name_plural = "Xodimlaring qo'shimcha dam olish turi"

    def __str__(self):
        return self.name


class Vacation(models.Model):
    vocation_period_type = (
        ('per_hour', 'Soatbay'),
        ('per_day', 'Kunbay')
    )
    vocation_period_types = models.CharField(choices=vocation_period_type, null=True, blank=True, max_length=255, verbose_name="Turi")
    start_at = models.DateField(verbose_name="Boshlash vaqti")
    end_at = models.DateField(verbose_name="Tugash vaqti")
    vacation_type = models.ForeignKey(VacationType, on_delete=models.CASCADE, verbose_name="Qo'shimcha dam olish turi")
    note = models.CharField(max_length=512, null=True, blank=True, verbose_name="Izoh")
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, verbose_name="Xodim")

    class Meta:
        verbose_name_plural = "Xodimlaring qo'shimcha dam olish bo'limi"

    def __str__(self):
        return f'{self.staff.first_name} {self.staff.second_name} {self.staff.last_name}'


class AdditionalPaymentType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kompaniya")
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Ushlab qolish yoki qo'shimcha to'lovlar nomi"

    def __str__(self):
        return self.name


class AdditionalPayments(models.Model):
    additional_payment = (
        ('find', "Ushlab qolish"),
        ('additional_payment', "Qo'shimcha to'lov")
    )
    apt = models.ForeignKey(AdditionalPaymentType, on_delete=models.CASCADE, verbose_name="Turi")
    attached_date = models.DateField(null=True, blank=True, verbose_name="Biriktirilgan sana")
    type_of_additional_payment = models.CharField(choices=additional_payment, max_length=225)
    amount = models.DecimalField(decimal_places=2 , max_digits=16, verbose_name="Summasi")
    note = models.TextField(verbose_name="Ta'rifi")
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, verbose_name="Xodim")

    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Ushlab qolish yoki to'lov qo'shish"

    def __str__(self):
        return f'{self.staff.first_name} {self.staff.second_name}'


class Flow(models.Model):
    came = models.DateTimeField(verbose_name="Kelishi")
    went = models.DateTimeField(verbose_name="Ketishi")
    staff = models.ForeignKey("Staff", on_delete=models.CASCADE, verbose_name="Xodim")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Hodimlarning kelib ketishi"

    def __str__(self):
        return f'{self.staff.first_name} {self.staff.second_name}'


class Document(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    date_of_issue = models.DateField(verbose_name="Berilgan sana")
    validity_period = models.DateField(verbose_name="Amal qilish mudati")
    document = models.FileField(upload_to='documents/', verbose_name="Hujjat(file)")
    note = models.CharField(max_length=255)
    staff = models.ForeignKey("Staff", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Hodim hujjatlari"

    def __str__(self):
        return self.name


class Salary(models.Model):
    type_of_work = models.CharField(null=True, blank=True, max_length=255,
                                    verbose_name="Ishlash turi(soatbay, kunbay, ishbay ...)")
    amount = models.FloatField(null=True, blank=True, verbose_name="Miqdori")
    attached_date = models.DateField(null=True, blank=True, verbose_name="Biriktirilgan sana")
    completion_date = models.DateField(null=True, blank=True, verbose_name="Yankunlangan sana")
    staff = models.ForeignKey("Staff", on_delete=models.CASCADE, verbose_name="Xodim")

    class Meta:
        verbose_name_plural = "Ish haqqi"

    def __str__(self):
        return self.type_of_work


class WorkPlan(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Ish Rejasi"

    def __str__(self):
        return self.name


class Staff(models.Model):
    GENDER = (
        ('male', 'Erkak'),
        ('female', 'Ayol')
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Kompaniya")
    first_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="Ism")
    second_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="Familiya")
    last_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="Otasining ismi")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    gender = models.CharField(choices=GENDER, max_length=10, verbose_name="Jinsi")

    tabel_number = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tabel raqami")
    start_work_at = models.DateField(null=True, blank=True, verbose_name="Ish boshlagan sana")
    account_number = models.BigIntegerField(null=True, blank=True, verbose_name="Xisob raqami")

    email = models.EmailField(unique=True, verbose_name="Elektron manzil")
    mobile_phone = models.CharField(null=True, blank=True, max_length=15, verbose_name="Mobil telefon")
    home_phone = models.CharField(null=True, blank=True, max_length=15, verbose_name="Uy telefoni")
    work_phone = models.CharField(null=True, blank=True, max_length=15, verbose_name="Ish telefoni")

    address = models.CharField(null=True, blank=True, max_length=255, verbose_name="Uy manzili")
    image = models.ImageField(upload_to='company/staff/image/', null=True, blank=True, verbose_name="Xodimning rasmi")
    qr_code = models.ImageField(upload_to='company/staff/qr_code/', null=True, blank=True, verbose_name="Xodimning qr code")

    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Bo'lim")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Lavozim")

    note = models.CharField(max_length=255, null=True, blank=True, verbose_name="Eslatma")
    work_plan = models.ForeignKey(WorkPlan, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Ish jadvali")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.first_name} {self.second_name} {self.last_name}')

    # def full_name(self):
    #     return f'{self.first_name} {self.second_name} {self.last_name}'

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Xodimlar"


# Vacancy&Answer&Question


class Question(models.Model):
    question = models.CharField(max_length=500, blank=True, null=True, verbose_name="Savol")
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Bo'lim savoli"


class NewStaff(models.Model):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Kompaniya")
    full_name = models.CharField(max_length=255, verbose_name="Xodimning to'liq ism sharifi")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Xodimning tug'ilgan sanasi")
    image = models.ImageField(upload_to='company/staff/image/', null=True, blank=True, verbose_name="Xodimning rasmi")
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE,
                                   verbose_name="Xodim ishlaydigan bo'lim")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name="Xodimning lavozimi")
    period_time = models.DateField(null=True, blank=True, verbose_name="Stajirovka mudati")
    phone_number = models.CharField(null=True, blank=True, max_length=50)
    address = models.CharField(null=True, blank=True, max_length=255)
    tg_user_id = models.IntegerField(null=True, blank=True)
    question_step = models.IntegerField(null=True, blank=True)
    tg_answer_id = models.IntegerField(null=True, blank=True)
    tg_username = models.CharField(null=True, blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name, field.value_to_string(self))

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Yangi xodimlar"


# answer + new conditae

class Answer(models.Model):
    candidate = models.ForeignKey(NewStaff, on_delete=models.CASCADE, verbose_name="Yangi Xodim")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Bo'lim savoli")
    answer = models.CharField(max_length=512, verbose_name="Javob")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Javoblar"


class Vacancy(models.Model):
    staff_position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Lavozimga vakansiya")
    description = fields.RichTextField(null=True, blank=True,
                                       verbose_name="Lavozimga qo'yiladigan talablar haqida ma'lumot")
    is_active = models.BooleanField(default=False, verbose_name="Vakansiya aktiv")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.staff_position.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Vakansiya"


class Bot(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Kompaniya")
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Bot nomi")
    token = models.CharField(max_length=512, null=True, blank=True, verbose_name="Token")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Bot"


class Admin(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Kompaniya")
    name = models.CharField(blank=True, null=True, max_length=255)
    chat_id = models.BigIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.chat_id)


class EntryText(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Kompaniya")
    name = models.CharField(blank=True, null=True, max_length=1024)

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class FinishText(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Kompaniya")
    name = models.CharField(blank=True, null=True, max_length=1024)

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


# class
