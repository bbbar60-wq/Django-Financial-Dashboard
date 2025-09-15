from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from .models import Payment, PaymentCategory, Course, Product, Student, Teacher, \
    BankAccount, Installment


def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def dashboard_view(request):
    return render(request, 'payments/dashboard.html')


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def payment_list(request):
    categories = PaymentCategory.objects.all()
    payments = Payment.objects.all()
    return render(request, 'payments/payment_list.html', {
        'categories': categories,
        'payments': payments
    })


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def payment_detail(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'payments/payment_detail.html', {
        'payment': payment
    })


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def filter_payments(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'GET' and is_ajax:
        category_id = request.GET.get('category_id')
        status_id = request.GET.get('status_id')
        payments = Payment.objects.all()

        if category_id:
            payments = payments.filter(category_id=category_id)
        if status_id:
            payments = payments.filter(status_id=status_id)

        data = [{
            'id': payment.id,
            'name': payment.name,
            'amount': str(payment.amount),
            'datetime': payment.datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'related_person': payment.related_person.name,
            'payment_method': payment.payment_method.title,
            'status': payment.status.title,
            'category': payment.category.name,
            'payment_type': payment.payment_type.title,
            'related_bank_account': payment.related_bank_account.name if payment.related_bank_account else None
        } for payment in payments]

        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def student_list(request):
    return render(request, 'payments/student_list.html')


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_students(request):
    students = Student.objects.all().values('name', 'national_id', 'id')
    return JsonResponse(list(students), safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def teacher_list(request):
    return render(request, 'payments/teacher_list.html')


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_teachers(request):
    teachers = Teacher.objects.all().values('name', 'national_id', 'id')
    return JsonResponse(list(teachers), safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def bank_account_list(request):
    return render(request, 'payments/bank_account_list.html')


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def product_list(request):
    return render(request, 'payments/product_list.html')


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_products(request):
    products = Product.objects.all().values('title', 'amount', 'teacher__name', 'id')
    return JsonResponse(list(products), safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def course_list(request):
    return render(request, 'payments/course_list.html')


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_courses(request):
    courses = Course.objects.all().values('title', 'session_time', 'start_date', 'end_date', 'teacher__name',
                                          'olympiad__title', 'id')
    return JsonResponse(list(courses), safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_payments(request):
    payments = Payment.objects.all().values('name', 'amount', 'id')
    return JsonResponse(list(payments), safe=False)


@csrf_protect
def login_view(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    attempts = request.session.get('login_attempts', 0)

    if attempts >= 5:
        return render(request, 'payments/login.html', {'error': 'Too many login attempts. Please try again later.'})

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username:
            return render(request, 'payments/login.html', {'error': 'Username is unfilled'})
        if not password:
            return render(request, 'payments/login.html', {'error': 'Password is unfilled'})

        user = authenticate(request, username=username, password=password)
        if user is not None and (user.is_staff or user.is_superuser):
            login(request, user)
            request.session['login_attempts'] = 0
            return redirect('dashboard')
        else:
            request.session['login_attempts'] = attempts + 1
            return render(request, 'payments/login.html',
                          {'error': 'Username or password is incorrect or you do not have access'})

    return render(request, 'payments/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    person = student.person

    payments = Payment.objects.filter(related_person=person).values(
        'name', 'amount', 'datetime', 'status__title',
        'payment_method__title', 'category__name',
        'payment_type__title', 'related_bank_account__name'
    )

    student_data = {
        'name': student.name,
        'national_id': student.national_id,
        'payments': list(payments)
    }
    return JsonResponse(student_data, safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    person = teacher.person

    payments = Payment.objects.filter(related_person=person).values(
        'name', 'amount', 'datetime', 'status__title',
        'payment_method__title', 'category__name',
        'payment_type__title', 'related_bank_account__name'
    )

    courses = Course.objects.filter(teacher=teacher).values(
        'title', 'session_time', 'start_date', 'end_date', 'olympiad__title'
    )
    products = Product.objects.filter(teacher=teacher).values(
        'title', 'amount', 'description'
    )

    teacher_data = {
        'name': teacher.name,
        'national_id': teacher.national_id,
        'payments': list(payments),
        'courses': list(courses),
        'products': list(products)
    }

    return JsonResponse(teacher_data, safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    products = Product.objects.filter(teacher=course.teacher).values('title', 'amount', 'description')

    course_data = {
        'title': course.title,
        'session_time': course.session_time,
        'start_date': course.start_date,
        'end_date': course.end_date,
        'teacher': course.teacher.name,
        'olympiad': course.olympiad.title if course.olympiad else 'None',
        'products': list(products)
    }
    return JsonResponse(course_data, safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    courses = Course.objects.filter(teacher=product.teacher).values('title', 'session_time', 'start_date', 'end_date',
                                                                    'olympiad__title')

    product_data = {
        'title': product.title,
        'amount': product.amount,
        'teacher': product.teacher.name,
        'courses': list(courses)
    }
    return JsonResponse(product_data, safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def bank_account_detail_page(request, bank_account_id):
    bank_account = get_object_or_404(BankAccount, id=bank_account_id)
    payments = Payment.objects.filter(related_bank_account=bank_account).values(
        'name', 'amount', 'datetime', 'status__title',
        'payment_method__title', 'category__name',
        'payment_type__title', 'related_person__name'
    )
    return render(request, 'payments/bank_account_detail.html', {
        'bank_account': bank_account,
        'payments': payments
    })


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_bank_accounts(request):
    bank_accounts = BankAccount.objects.all().values('id', 'name', 'bank_number')
    bank_accounts_list = list(bank_accounts)

    # Add related payments to each bank account
    for bank_account in bank_accounts_list:
        payments = Payment.objects.filter(related_bank_account_id=bank_account['id']).values(
            'name', 'amount', 'datetime', 'status__title',
            'payment_method__title', 'category__name',
            'payment_type__title', 'related_person__name'
        )
        bank_account['payments'] = list(payments)

    return JsonResponse(bank_accounts_list, safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_payment_detail(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    payment_data = {
        'name': payment.name,
        'amount': payment.amount,
        'datetime': payment.datetime,
        'status': payment.status.title,
        'payment_method': payment.payment_method.title,
        'category': payment.category.name,
        'payment_type': payment.payment_type.title,
        'related_person': payment.related_person.name,
        'related_bank_account': payment.related_bank_account.name if payment.related_bank_account else None
    }
    return JsonResponse(payment_data, safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_bank_account_detail(request, bank_account_id):
    bank_account = get_object_or_404(BankAccount, id=bank_account_id)
    payments = Payment.objects.filter(related_bank_account=bank_account).values(
        'name', 'amount', 'datetime', 'status__title',
        'payment_method__title', 'category__name',
        'payment_type__title', 'related_person__name'
    )
    data = {
        'name': bank_account.name,
        'bank_number': bank_account.bank_number,
        'payments': list(payments)
    }
    return JsonResponse(data, safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def teacher_detail_page(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    person = teacher.person

    payments = Payment.objects.filter(related_person=person).values(
        'name', 'amount', 'datetime', 'status__title',
        'payment_method__title', 'category__name',
        'payment_type__title', 'related_bank_account__name'
    )

    courses = Course.objects.filter(teacher=teacher).values(
        'title', 'session_time', 'start_date', 'end_date', 'olympiad__title'
    )

    products = Product.objects.filter(teacher=teacher).values(
        'title', 'amount', 'description'
    )

    return render(request, 'payments/teacher_detail.html', {
        'teacher': teacher,
        'payments': payments,
        'courses': courses,
        'products': products
    })


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def student_detail_page(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    person = student.person

    payments = Payment.objects.filter(related_person=person).values(
        'name', 'amount', 'datetime', 'status__title',
        'payment_method__title', 'category__name',
        'payment_type__title', 'related_bank_account__name'
    )

    return render(request, 'payments/student_detail.html', {
        'student': student,
        'payments': payments
    })


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def course_detail_page(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    products = Product.objects.filter(teacher=course.teacher).values('title', 'amount', 'description')

    return render(request, 'payments/course_detail.html', {
        'course': course,
        'products': products
    })


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def product_detail_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    courses = Course.objects.filter(teacher=product.teacher).values('title', 'session_time', 'start_date', 'end_date',
                                                                    'olympiad__title')

    return render(request, 'payments/product_detail.html', {
        'product': product,
        'courses': courses
    })


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def payment_list(request):
    categories = PaymentCategory.objects.all()
    payments = Payment.objects.all()
    return render(request, 'payments/payment_list.html', {
        'categories': categories,
        'payments': payments
    })


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def payment_detail(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'payments/payment_detail.html', {
        'payment': payment
    })


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_payments(request):
    payments = Payment.objects.all().values('id', 'name', 'amount', 'datetime', 'status__title',
                                            'payment_method__title', 'category__name', 'payment_type__title',
                                            'related_person__name', 'related_bank_account__name')
    return JsonResponse(list(payments), safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_payment_detail(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment_data = {
        'id': payment.id,
        'name': payment.name,
        'amount': payment.amount,
        'datetime': payment.datetime.strftime('%Y-%m-%d %H:%M:%S'),
        'status': payment.status.title,
        'payment_method': payment.payment_method.title,
        'category': payment.category.name,
        'payment_type': payment.payment_type.title,
        'related_person': payment.related_person.name,
        'related_bank_account': payment.related_bank_account.name if payment.related_bank_account else None,
        'info_text': payment.info_text
    }
    return JsonResponse(payment_data, safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def installment_list(request):
    return render(request, 'payments/installment_list.html')


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_installments(request):
    installments = Installment.objects.all().values(
        'id', 'amount', 'due_date', 'received_date', 'status__title', 'payment_agreement__id'
    )
    return JsonResponse(list(installments), safe=False)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def installment_detail_page(request, installment_id):
    installment = get_object_or_404(Installment, id=installment_id)
    return render(request, 'payments/installment_detail.html', {
        'installment': installment
    })


@login_required
@user_passes_test(is_staff_or_superuser, login_url='login')
def api_installment_detail(request, installment_id):
    installment = get_object_or_404(Installment, id=installment_id)
    installment_data = {
        'id': installment.id,
        'amount': installment.amount,
        'due_date': installment.due_date.strftime('%Y-%m-%d %H:%M:%S'),
        'received_date': installment.received_date.strftime('%Y-%m-%d %H:%M:%S') if installment.received_date else None,
        'status': installment.status.title if installment.status else None,
        'payment_agreement_id': installment.payment_agreement.id,
    }
    return JsonResponse(installment_data, safe=False)
