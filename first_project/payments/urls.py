from django.urls import path
from . import views
from .admin import ExcelUploadAdmin

urlpatterns = [
    path('students/', views.student_list, name='student_list'),
    path('api/students/', views.api_students, name='api_students'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('api/teachers/', views.api_teachers, name='api_teachers'),
    path('bank-accounts/', views.bank_account_list, name='bank_account_list'),
    path('api/bank-accounts/', views.api_bank_accounts, name='api_bank_accounts'),
    path('products/', views.product_list, name='product_list'),
    path('api/products/', views.api_products, name='api_products'),
    path('courses/', views.course_list, name='course_list'),
    path('api/courses/', views.api_courses, name='api_courses'),
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('student-detail/<int:student_id>/', views.student_detail_page, name='student_detail'),
    path('teacher-detail/<int:teacher_id>/', views.teacher_detail_page, name='teacher_detail'),
    path('course-detail/<int:course_id>/', views.course_detail_page, name='course_detail'),
    path('product-detail/<int:product_id>/', views.product_detail_page, name='product_detail'),
    path('bank-account-detail/<int:bank_account_id>/', views.bank_account_detail_page, name='bank_account_detail'),
    path('payments/', views.payment_list, name='payment_list'),
    path('payment-detail/<int:payment_id>/', views.payment_detail, name='payment_detail'),
    path('api/payments/', views.api_payments, name='api_payments'),
    path('api/payment-detail/<int:payment_id>/', views.api_payment_detail, name='api_payment_detail'),
    path('installments/', views.installment_list, name='installment_list'),
    path('api/installments/', views.api_installments, name='api_installments'),
    path('installment-detail/<int:installment_id>/', views.installment_detail_page, name='installment_detail'),
    path('api/installment-detail/<int:installment_id>/', views.api_installment_detail, name='api_installment_detail'),
    path('admin/upload-excel/', ExcelUploadAdmin.upload_excel, name='upload_excel'),
]
