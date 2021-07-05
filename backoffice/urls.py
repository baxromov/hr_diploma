from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainTemplate.as_view(), name="backoffice-main"),
    path('table', views.TableTemplate.as_view(), name="table"),
    path('login', views.LoginPage.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('registration', views.Registration.as_view(), name="registration"),

    # Staff
    path('staff', views.StaffListTemplate.as_view(), name="staff"),
    path('staff/create', views.StaffCreate.as_view(), name="staff_create"),
    path('staff/<int:pk>', views.StaffUpdate.as_view(), name="staff-detail"),
    path('staff/delete/<int:pk>', views.StaffDeleteView.as_view(), name="staff_delete"),

    # Position
    path('position/create', views.PositionCreateView.as_view(), name="position_create"),
    path('position', views.PositionListView.as_view(), name="position"),
    path('position/update/<int:pk>', views.PositionUpdateView.as_view(), name="position_update"),
    path('position/delete/<int:pk>', views.PositionDeleteView.as_view(), name="position_delete"),

    # StaffORGSystem
    path('staff-org-system/create', views.StaffORGSystemCreateView.as_view(), name="staff_org_system_create"),
    path('staff-org-system', views.StaffORGSystemListView.as_view(), name="staff_org_system"),
    path('staff-org-system/update/<int:pk>', views.StaffORGSystemUpdateView.as_view(), name="staff_org_system_update"),
    path('staff-org-system/delete/<int:pk>', views.StaffORGSystemDeleteView.as_view(), name="staff_org_system_delete"),

    # Department URL
    path('department', views.DepartmentListView.as_view(), name='department'),
    path('department/create', views.DepartmentCreateView.as_view(), name='department_create'),
    path('department/update/<int:pk>', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('department/delete/<int:pk>', views.DepartmentDeleteView.as_view(), name='department_delete'),

    # Salary
    path('salary/<int:pk>', views.SalaryListView.as_view(), name='salary'),
    path('salary/create', views.SalaryCreateView.as_view(), name='salary_create'),
    path('salary/update/<int:pk>', views.SalaryUpdateView.as_view(), name='salary_update'),
    path('salary/delete/<int:pk>', views.SalaryDeleteView.as_view(), name='salary_delete'),

    # Vacation
    path('vacation/<int:pk>', views.VacationCreateView.as_view(), name='vacation'),
    path('vacation/update/<int:pk>', views.VacationUpdateView.as_view(), name='vacation_update'),
    path('vacation/delete/<int:pk>', views.VacationDeleteView.as_view(), name='vacation_delete'),

    # VacationTypeType
    path('vacation-type', views.VacationTypeTypeListView.as_view(), name='vacation_type'),
    path('vacation-type/create', views.VacationTypeCreateView.as_view(), name='vacation_type_create'),
    path('vacation-type/update/<int:pk>', views.VacationTypeUpdateView.as_view(), name='vacation_type_update'),
    path('vacation-type/delete/<int:pk>', views.VacationTypeDeleteView.as_view(), name='vacation_type_delete'),

    # AdditionalPayments
    path('additional-payment/<int:pk>', views.AdditionalPaymentsCreateView.as_view(), name='additional_payment'),
    path('additional-payment/update/<int:pk>', views.AdditionalPaymentsUpdateView.as_view(), name='additional_payment_update'),
    path('additional-payment/delete/<int:pk>', views.AdditionalPaymentsDeleteView.as_view(), name='additional_payment_delete'),

    # AdditionalPaymentsType
    path('additional-payment-type', views.AdditionalPaymentsTypeListView.as_view(), name='additional_payment_type'),
    path('additional-payment-type/create', views.AdditionalPaymentsTypeCreateView.as_view(), name='additional_payment_type_create'),
    path('additional-payment-type/update/<int:pk>', views.AdditionalPaymentsTypeUpdateView.as_view(), name='additional_payment_type_update'),
    path('additional-payment-type/delete/<int:pk>', views.AdditionalPaymentsTypeDeleteView.as_view(), name='additional_payment_type_delete'),

    # Document
    path('document/<int:pk>', views.DocumentListCreateView.as_view(), name='document'),
    path('document/update/<int:pk>', views.DocumentUpdateView.as_view(), name='document_update'),
    path('document/delete/<int:pk>', views.DocumentDeleteView.as_view(), name='document_delete'),

    # setting
    path('settings', views.Settings.as_view(), name='settings'),

    # NewTelegramStaffListView
    path('new-telegram-staff', views.NewTelegramStaffListView.as_view(), name="new_telegram_staff"),
    path('new-telegram-staff/<int:pk>', views.NewTelegramStaffDetailView.as_view(), name="new_telegram_staff_detail"),

    # Bot
    path('settings/bot', views.BotListView.as_view(), name='bot_c_l'),
    path('settings/bot/<int:pk>', views.BotUpdateView.as_view(), name='bot_c_u'),

    # Admin
    path('settings/admin-bot', views.AdminCreateView.as_view(), name='admin_bot'),
    path('settings/admin-bot/delete/<int:pk>', views.AdminDeleteView.as_view(), name='admin_bot_delete'),
    path('settings/admin-bot/update/<int:pk>', views.AdminUpdateView.as_view(), name='admin_bot_update'),

    # EntryText
    path('settings/entry-text', views.EntryTextCreateView.as_view(), name='entry_text'),
    path('settings/entry-text/delete/<int:pk>', views.EntryTextDeleteView.as_view(), name='entry_text_delete'),
    path('settings/entry-text/update/<int:pk>', views.EntryTextUpdateView.as_view(), name='entry_text_update'),

    # FinishText
    path('settings/finish-text', views.FinishTextCreateView.as_view(), name='finish_text'),
    path('settings/finish-text/delete/<int:pk>', views.FinishTextDeleteView.as_view(), name='finish_text_delete'),
    path('settings/finish-text/update/<int:pk>', views.FinishTexttUpdateView.as_view(), name='finish_text_update'),

    # Company
    path('info', views.CompanyTemplateView.as_view(), name='info'),
    path('company/<int:pk>', views.CompanyUpdate.as_view(), name='company_update'),

    # Searching Staff
    path('search-staff', views.SearchingStaffListView.as_view(), name='search_staff'),

    # Controlling staff flow
    path('control-staff-flow', views.ControlFlowingStaffTemplateView.as_view(), name='control_staff_flow'),

    # TrainingInfo
    path('training-info', views.TrainingInfoTemplateView.as_view(), name="training_info"),
    path('training-info/delete/<int:pk>', views.TrainingInfoDeleteView.as_view(), name="training_info_delete"),
    path('training-info/update/<int:pk>', views.TrainingInfoUpdateView.as_view(), name="training_info_update"),

    # CompanyCulture
    path('company-culture', views.CompanyCultureCreateViewListView.as_view(), name="company_culture"),
    path('company-culture/delete/<int:pk>', views.CompanyCultureDeleteView.as_view(), name="company_culture_delete"),
    path('company-culture/update/<int:pk>', views.CompanyCultureUpdateView.as_view(), name="company_culture_update"),

    # CompanySchedule
    path('company-schedule', views.CompanyScheduleCreateViewListView.as_view(), name="company_schedule"),
    path('company-schedule/delete/<int:pk>', views.CompanyScheduleDeleteView.as_view(), name="company_schedule_delete"),
    path('company-schedule/update/<int:pk>', views.CompanyScheduleUpdateView.as_view(), name="company_schedule_update"),

    # TrainingAnswerListView
    path('staff-training-answer', views.TrainingAnswerListView.as_view(), name="staff_training_answer"),

    # Super Staff
    path('super-staff', views.SuperStaffCreateView.as_view(), name='super_staff'),
    path('super-staff/delete/<int:pk>', views.SuperStaffDeleteView.as_view(), name='super_staff_delete'),
    path('super-staff/update/<int:pk>', views.SuperStaffUpdateView.as_view(), name='super_staff_update'),

]
