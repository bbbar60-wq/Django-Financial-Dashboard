from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import views as auth_views
from .models import (
    Person, BankAccount, PaymentMethod, PaymentType, Status,
    PaymentCategory, Payment, Student, Teacher, Olympiad, Course, Product,
    StudentAgreement, TeacherAgreement, PaymentAgreement, Installment, InstallmentStatus, PaymentFile
)
import pandas as pd


def staff_or_superuser_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_active and (u.is_staff or u.is_superuser),
        login_url='/admin/login/'
    )(view_func)
    return decorated_view_func


@staff_or_superuser_required
def custom_admin_index(request):
    return admin.site.index(request)


@staff_or_superuser_required
def custom_admin_app_index(request, app_label):
    return admin.site.app_index(request, app_label)


def custom_admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/admin/')
    return auth_views.LoginView.as_view(template_name='admin/login.html')(request)


def custom_admin_logout(request):
    return auth_views.LogoutView.as_view(next_page='/admin/login/')(request)


class ExcelUploadAdmin(admin.ModelAdmin):
    change_list_template = "admin/excel_upload_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/', self.admin_site.admin_view(self.upload_excel),
                 name=f'{self.model.__name__.lower()}_upload_excel'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['model_name'] = self.model.__name__.lower()
        return super().changelist_view(request, extra_context=extra_context)

    def upload_excel(self, request):
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            excel_file = request.FILES.get('file')
            if excel_file:
                try:
                    df = pd.read_excel(excel_file)
                    if df.empty:
                        return JsonResponse({'success': False, 'message': 'The Excel file is empty.'})
                    model = self.model
                    self.process_excel_data(df, model)
                    return JsonResponse(
                        {'success': True, 'message': 'Excel file uploaded and data processed successfully!'})
                except Exception as e:
                    return JsonResponse({'success': False, 'message': f'Error processing Excel file: {e}'})
            else:
                return JsonResponse({'success': False, 'message': 'No file uploaded.'})
        else:
            return render(request, 'admin/upload_excel.html', {'model_name': self.model.__name__.lower()})

    def process_excel_data(self, df, model):
        for index, row in df.iterrows():
            if row.isnull().all():
                continue
            if model == Person:
                self.process_person(row)
            elif model == BankAccount:
                self.process_bank_account(row)
            elif model == PaymentMethod:
                self.process_payment_method(row)
            elif model == PaymentType:
                self.process_payment_type(row)
            elif model == Status:
                self.process_status(row)
            elif model == PaymentCategory:
                self.process_payment_category(row)
            elif model == Payment:
                self.process_payment(row)
            elif model == Student:
                self.process_student(row)
            elif model == Teacher:
                self.process_teacher(row)
            elif model == Olympiad:
                self.process_olympiad(row)
            elif model == Product:
                self.process_product(row)
            elif model == Course:
                self.process_course(row)
            elif model == StudentAgreement:
                self.process_student_agreement(row)
            elif model == TeacherAgreement:
                self.process_teacher_agreement(row)
            elif model == PaymentAgreement:
                self.process_payment_agreement(row)
            elif model == Installment:
                self.process_installment(row)
            elif model == InstallmentStatus:
                self.process_installment_status(row)
            elif model == PaymentFile:
                self.process_payment_file(row)

    def process_person(self, row):
        person_name = row['person_name'] if pd.notna(row['person_name']) else None
        person_national_id = row['person_national_id'] if pd.notna(row['person_national_id']) else None
        if person_name and person_national_id:
            Person.objects.get_or_create(name=person_name, national_id=person_national_id)

    def process_bank_account(self, row):
        bank_name = row['bank_name'] if pd.notna(row['bank_name']) else None
        bank_number = row['bank_number'] if pd.notna(row['bank_number']) else None
        bank_description = row['bank_description'] if pd.notna(row['bank_description']) else None
        if bank_name and bank_number:
            BankAccount.objects.get_or_create(name=bank_name, bank_number=bank_number,
                                              defaults={'description': bank_description})

    def process_payment_method(self, row):
        title = row['title'] if pd.notna(row['title']) else None
        description = row['description'] if pd.notna(row['description']) else None
        if title:
            PaymentMethod.objects.get_or_create(title=title, defaults={'description': description})

    def process_payment_type(self, row):
        title = row['title'] if pd.notna(row['title']) else None
        description = row['description'] if pd.notna(row['description']) else None
        if title:
            PaymentType.objects.get_or_create(title=title, defaults={'description': description})

    def process_status(self, row):
        title = row['title'] if pd.notna(row['title']) else None
        description = row['description'] if pd.notna(row['description']) else None
        if title:
            Status.objects.get_or_create(title=title, defaults={'description': description})

    def process_payment_category(self, row):
        name = row['name'] if pd.notna(row['name']) else None
        type = row['type'] if pd.notna(row['type']) else None
        if name:
            PaymentCategory.objects.get_or_create(name=name, defaults={'type': type})

    def process_payment(self, row):
        name = row['name'] if pd.notna(row['name']) else None
        amount = row['amount'] if pd.notna(row['amount']) else None
        related_person = Person.objects.filter(id=row['related_person']).first() if pd.notna(
            row['related_person']) else None
        payment_method = PaymentMethod.objects.filter(id=row['payment_method']).first() if pd.notna(
            row['payment_method']) else None
        status = Status.objects.filter(id=row['status']).first() if pd.notna(row['status']) else None
        category = PaymentCategory.objects.filter(id=row['category']).first() if pd.notna(row['category']) else None
        payment_type = PaymentType.objects.filter(id=row['payment_type']).first() if pd.notna(
            row['payment_type']) else None
        related_bank_account = BankAccount.objects.filter(id=row['related_bank_account']).first() if pd.notna(
            row['related_bank_account']) else None

        if not payment_type:
            raise ValueError(f"Payment type is missing or invalid for payment: {name}")

        if name and amount:
            Payment.objects.get_or_create(
                name=name,
                amount=amount,
                related_person=related_person,
                payment_method=payment_method,
                status=status,
                category=category,
                payment_type=payment_type,
                related_bank_account=related_bank_account
            )

    def process_student(self, row):
        name = row['name'] if pd.notna(row['name']) else None
        national_id = row['national_id'] if pd.notna(row['national_id']) else None
        person = Person.objects.filter(id=row['person']).first() if pd.notna(row['person']) else None
        if name and national_id and person:
            Student.objects.get_or_create(name=name, national_id=national_id, person=person)

    def process_teacher(self, row):
        name = row['name'] if pd.notna(row['name']) else None
        national_id = row['national_id'] if pd.notna(row['national_id']) else None
        person = Person.objects.filter(id=row['person']).first() if pd.notna(row['person']) else None
        if name and national_id and person:
            Teacher.objects.get_or_create(name=name, national_id=national_id, person=person)

    def process_olympiad(self, row):
        title = row['title'] if pd.notna(row['title']) else None
        if title:
            Olympiad.objects.get_or_create(title=title)

    def process_product(self, row):
        title = row['title'] if pd.notna(row['title']) else None
        description = row['description'] if pd.notna(row['description']) else None
        amount = row['amount'] if pd.notna(row['amount']) else None
        teacher = Teacher.objects.filter(id=row['teacher']).first() if pd.notna(row['teacher']) else None
        if title and teacher:
            Product.objects.get_or_create(title=title, teacher=teacher,
                                          defaults={'description': description, 'amount': amount})

    def process_course(self, row):
        title = row['title'] if pd.notna(row['title']) else None
        session_time = row['session_time'] if pd.notna(row['session_time']) else None
        start_date = row['start_date'] if pd.notna(row['start_date']) else None
        end_date = row['end_date'] if pd.notna(row['end_date']) else None
        teacher = Teacher.objects.filter(id=row['teacher']).first() if pd.notna(row['teacher']) else None
        olympiad = Olympiad.objects.filter(id=row['olympiad']).first() if pd.notna(row['olympiad']) else None
        if title and teacher:
            Course.objects.get_or_create(
                title=title,
                session_time=session_time,
                start_date=start_date,
                end_date=end_date,
                teacher=teacher,
                olympiad=olympiad
            )

    def process_student_agreement(self, row):
        student = Student.objects.filter(id=row['student']).first() if pd.notna(row['student']) else None
        course = Course.objects.filter(id=row['course']).first() if pd.notna(row['course']) else None
        amount = row['amount'] if pd.notna(row['amount']) else None
        attrs = row['attrs'] if pd.notna(row['attrs']) else None
        if student and course:
            StudentAgreement.objects.get_or_create(student=student, course=course,
                                                   defaults={'amount': amount, 'attrs': attrs})

    def process_teacher_agreement(self, row):
        teacher = Teacher.objects.filter(id=row['teacher']).first() if pd.notna(row['teacher']) else None
        product = Product.objects.filter(id=row['product']).first() if pd.notna(row['product']) else None
        amount = row['amount'] if pd.notna(row['amount']) else None
        attrs = row['attrs'] if pd.notna(row['attrs']) else None
        if teacher and product:
            TeacherAgreement.objects.get_or_create(teacher=teacher, product=product,
                                                   defaults={'amount': amount, 'attrs': attrs})

    def process_payment_agreement(self, row):
        student_agreement = StudentAgreement.objects.filter(id=row['student_agreement']).first() if pd.notna(
            row['student_agreement']) else None
        teacher_agreement = TeacherAgreement.objects.filter(id=row['teacher_agreement']).first() if pd.notna(
            row['teacher_agreement']) else None
        payment_direction = row['payment_direction'] if pd.notna(row['payment_direction']) else 'in'
        total_amount = row['total_amount'] if pd.notna(row['total_amount']) else None
        if student_agreement or teacher_agreement:
            PaymentAgreement.objects.get_or_create(
                student_agreement=student_agreement,
                teacher_agreement=teacher_agreement,
                defaults={'payment_direction': payment_direction, 'total_amount': total_amount}
            )

    def process_installment(self, row):
        payment_agreement = PaymentAgreement.objects.filter(id=row['payment_agreement']).first() if pd.notna(
            row['payment_agreement']) else None
        amount = row['amount'] if pd.notna(row['amount']) else None
        due_date = row['due_date'] if pd.notna(row['due_date']) else None
        received_date = row['received_date'] if pd.notna(row['received_date']) else None
        status = InstallmentStatus.objects.filter(id=row['status']).first() if pd.notna(row['status']) else None
        if payment_agreement and amount and due_date:
            Installment.objects.get_or_create(
                payment_agreement=payment_agreement,
                amount=amount,
                due_date=due_date,
                defaults={'received_date': received_date, 'status': status}
            )

    def process_installment_status(self, row):
        title = row['title'] if pd.notna(row['title']) else None
        if title:
            InstallmentStatus.objects.get_or_create(title=title)

    def process_payment_file(self, row):
        payment = Payment.objects.filter(id=row['payment']).first() if pd.notna(row['payment']) else None
        file = row['file'] if pd.notna(row['file']) else None
        if payment and file:
            PaymentFile.objects.get_or_create(payment=payment, file=file)


@admin.register(Person)
class PersonAdmin(ExcelUploadAdmin):
    list_display = ['name', 'national_id']
    search_fields = ['name', 'national_id']


@admin.register(BankAccount)
class BankAccountAdmin(ExcelUploadAdmin):
    list_display = ['name', 'bank_number']
    search_fields = ['name', 'bank_number']


@admin.register(PaymentMethod)
class PaymentMethodAdmin(ExcelUploadAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']


@admin.register(PaymentType)
class PaymentTypeAdmin(ExcelUploadAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']


@admin.register(Status)
class StatusAdmin(ExcelUploadAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']


@admin.register(PaymentCategory)
class PaymentCategoryAdmin(ExcelUploadAdmin):
    list_display = ['name', 'type']
    search_fields = ['name', 'type']


@admin.register(Payment)
class PaymentAdmin(ExcelUploadAdmin):
    list_display = ['name', 'amount', 'category', 'payment_type', 'status', 'related_person', 'related_bank_account']
    list_filter = ['payment_type', 'status', 'category', 'payment_method']
    search_fields = ['name', 'related_person__name', 'related_bank_account__name']
    autocomplete_fields = ['related_person', 'related_bank_account', 'payment_method', 'payment_type', 'status']


@admin.register(PaymentFile)
class PaymentFileAdmin(ExcelUploadAdmin):
    list_display = ['payment', 'file']
    autocomplete_fields = ['payment']


@admin.register(Student)
class StudentAdmin(ExcelUploadAdmin):
    list_display = ['name', 'national_id']
    search_fields = ['name', 'national_id']
    autocomplete_fields = ['person']


@admin.register(Teacher)
class TeacherAdmin(ExcelUploadAdmin):
    list_display = ['name', 'national_id']
    search_fields = ['name', 'national_id']
    autocomplete_fields = ['person']


@admin.register(Olympiad)
class OlympiadAdmin(ExcelUploadAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Course)
class CourseAdmin(ExcelUploadAdmin):
    list_display = ['title', 'session_time', 'start_date', 'end_date', 'teacher', 'olympiad']
    search_fields = ['title', 'teacher__name', 'olympiad__title']
    autocomplete_fields = ['teacher', 'olympiad']


@admin.register(Product)
class ProductAdmin(ExcelUploadAdmin):
    list_display = ['title', 'amount', 'teacher']
    search_fields = ['title', 'teacher__name']
    autocomplete_fields = ['teacher']


@admin.register(StudentAgreement)
class StudentAgreementAdmin(ExcelUploadAdmin):
    list_display = ['student', 'course', 'agreement_date', 'amount', 'attrs']
    search_fields = ['student__name', 'course__title']
    autocomplete_fields = ['student', 'course']


@admin.register(TeacherAgreement)
class TeacherAgreementAdmin(ExcelUploadAdmin):
    list_display = ['teacher', 'product', 'agreement_date', 'amount', 'attrs']
    search_fields = ['teacher__name', 'product__title']
    autocomplete_fields = ['teacher', 'product']


@admin.register(PaymentAgreement)
class PaymentAgreementAdmin(ExcelUploadAdmin):
    list_display = ['id', 'student_agreement', 'teacher_agreement', 'payment_direction', 'total_amount']
    search_fields = ['student_agreement__id', 'teacher_agreement__id']
    list_filter = ['payment_direction']
    autocomplete_fields = ['student_agreement', 'teacher_agreement']


@admin.register(Installment)
class InstallmentAdmin(ExcelUploadAdmin):
    list_display = ['id', 'payment_agreement', 'amount', 'due_date', 'received_date', 'status']
    search_fields = ['payment_agreement__id']
    list_filter = ['status', 'due_date']
    autocomplete_fields = ['payment_agreement']


@admin.register(InstallmentStatus)
class InstallmentStatusAdmin(ExcelUploadAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']


admin.site.index = staff_or_superuser_required(admin.site.index)
admin.site.app_index = staff_or_superuser_required(admin.site.app_index)
admin.site.login = custom_admin_login
admin.site.logout = custom_admin_logout
