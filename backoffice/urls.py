from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainTemplate.as_view(), name="backoffice-main"),
    path('table', views.TableTemplate.as_view(), name="table"),
    path('login', views.LoginPage.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('registration', views.Registration.as_view(), name="registration"),
]

# Staff
urlpatterns += [
    path('staff', views.StaffListTemplate.as_view(), name="staff"),
    path('staff/create', views.StaffCreate.as_view(), name="staff_create"),
    path('staff/<int:pk>', views.StaffUpdate.as_view(), name="staff-detail"),
    path('staff/delete/<int:pk>', views.StaffDeleteView.as_view(), name="staff_delete"),

]

# Position
urlpatterns += [
    path('position/create', views.PositionCreateView.as_view(), name="position_create"),
    path('position', views.PositionListView.as_view(), name="position"),
    path('position/update/<int:pk>', views.PositionUpdateView.as_view(), name="position_update"),
    path('position/delete/<int:pk>', views.PositionDeleteView.as_view(), name="position_delete"),
]

# Department URL
urlpatterns += [
    path('department', views.DepartmentListView.as_view(), name='department'),
    path('department/create', views.DepartmentCreateView.as_view(), name='department_create'),
    path('department/update/<int:pk>', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('department/delete/<int:pk>', views.DepartmentDeleteView.as_view(), name='department_delete'),
]

# Salary
urlpatterns += [
    path('salary/<int:pk>', views.SalaryListView.as_view(), name='salary'),
    path('salary/create', views.SalaryCreateView.as_view(), name='salary_create'),
    path('salary/update/<int:pk>', views.SalaryUpdateView.as_view(), name='salary_update'),
    path('salary/delete/<int:pk>', views.SalaryDeleteView.as_view(), name='salary_delete'),
]

# Vacation
urlpatterns += [
    path('vacation/<int:pk>', views.VacationCreateView.as_view(), name='vacation'),
    path('vacation/update/<int:pk>', views.VacationUpdateView.as_view(), name='vacation_update'),
    path('vacation/delete/<int:pk>', views.VacationDeleteView.as_view(), name='vacation_delete'),
]

# VacationTypeType
urlpatterns += [
    path('vacation-type', views.VacationTypeTypeListView.as_view(), name='vacation_type'),
    path('vacation-type/create', views.VacationTypeCreateView.as_view(), name='vacation_type_create'),
    path('vacation-type/update/<int:pk>', views.VacationTypeUpdateView.as_view(), name='vacation_type_update'),
    path('vacation-type/delete/<int:pk>', views.VacationTypeDeleteView.as_view(), name='vacation_type_delete'),
]


# AdditionalPayments
urlpatterns += [
    path('additional-payment/<int:pk>', views.AdditionalPaymentsCreateView.as_view(), name='additional_payment'),
    path('additional-payment/update/<int:pk>', views.AdditionalPaymentsUpdateView.as_view(), name='additional_payment_update'),
    path('additional-payment/delete/<int:pk>', views.AdditionalPaymentsDeleteView.as_view(), name='additional_payment_delete'),
]

# AdditionalPaymentsType
urlpatterns += [
    path('additional-payment-type', views.AdditionalPaymentsTypeListView.as_view(), name='additional_payment_type'),
    path('additional-payment-type/create', views.AdditionalPaymentsTypeCreateView.as_view(), name='additional_payment_type_create'),
    path('additional-payment-type/update/<int:pk>', views.AdditionalPaymentsTypeUpdateView.as_view(), name='additional_payment_type_update'),
    path('additional-payment-type/delete/<int:pk>', views.AdditionalPaymentsTypeDeleteView.as_view(), name='additional_payment_type_delete'),
]

# Document
urlpatterns += [
    path('document/<int:pk>', views.DocumentListCreateView.as_view(), name='document'),
    path('document/update/<int:pk>', views.DocumentUpdateView.as_view(), name='document_update'),
    path('document/delete/<int:pk>', views.DocumentDeleteView.as_view(), name='document_delete'),
]

# ---------------------------------------------------------------------------------------------------------------------

urlpatterns += [
    path('settings', views.Settings.as_view(), name='settings'),
]

# NewTelegramStaffListView
urlpatterns += [
    path('new-telegram-staff', views.NewTelegramStaffListView.as_view(), name="new_telegram_staff"),
    path('new-telegram-staff/<int:pk>', views.NewTelegramStaffDetailView.as_view(), name="new_telegram_staff_detail"),
]

# Bot
urlpatterns += [
    path('settings/bot', views.BotListView.as_view(), name='bot_c_l'),
    path('settings/bot/<int:pk>', views.BotUpdateView.as_view(), name='bot_c_u'),
]

# Admin
urlpatterns += [
    path('settings/admin-bot', views.AdminCreateView.as_view(), name='admin_bot'),
    path('settings/admin-bot/delete/<int:pk>', views.AdminDeleteView.as_view(), name='admin_bot_delete'),
    path('settings/admin-bot/update/<int:pk>', views.AdminUpdateView.as_view(), name='admin_bot_update'),
]

# EntryText
urlpatterns += [
    path('settings/entry-text', views.EntryTextCreateView.as_view(), name='entry_text'),
    path('settings/entry-text/delete/<int:pk>', views.EntryTextDeleteView.as_view(), name='entry_text_delete'),
    path('settings/entry-text/update/<int:pk>', views.EntryTextUpdateView.as_view(), name='entry_text_update'),
]

# FinishText
urlpatterns += [
    path('settings/finish-text', views.FinishTextCreateView.as_view(), name='finish_text'),
    path('settings/finish-text/delete/<int:pk>', views.FinishTextDeleteView.as_view(), name='finish_text_delete'),
    path('settings/finish-text/update/<int:pk>', views.FinishTexttUpdateView.as_view(), name='finish_text_update'),
]

# Company
urlpatterns += [
    path('info', views.CompanyTemplateView.as_view(), name='info'),
    path('company/<int:pk>', views.CompanyUpdate.as_view(), name='company_update')
]

# Searching Staff
urlpatterns += [
    path('search-staff', views.SearchingStaffListView.as_view(), name='search_staff')
]

# Controlling staff flow
urlpatterns += [
    path('control-staff-flow', views.ControlFlowingStaffTemplateView.as_view(), name='control_staff_flow')
]

# TrainingInfo
urlpatterns += [
    path('training-info', views.TrainingInfoTemplateView.as_view(), name="training_info"),
    path('training-info/delete/<int:pk>', views.TrainingInfoDeleteView.as_view(), name="training_info_delete"),
    path('training-info/update/<int:pk>', views.TrainingInfoUpdateView.as_view(), name="training_info_update"),
]
