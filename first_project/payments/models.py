from django.db import models
from django.core.exceptions import ValidationError


class Person(models.Model):
    name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=20, unique=True)

    def clean(self):
        if not self.national_id.isdigit():
            raise ValidationError("National ID must contain only digits.")

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    name = models.CharField(max_length=255)
    bank_number = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def clean(self):
        if not self.bank_number.isdigit():
            raise ValidationError("Bank number must contain only digits.")

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class PaymentType(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Status(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class PaymentCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    related_person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name='payments')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING, related_name='payments')
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='payments')
    info_text = models.TextField(blank=True, null=True)
    category = models.ForeignKey(PaymentCategory, on_delete=models.DO_NOTHING, related_name='payments')
    payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING, related_name='payments')
    related_bank_account = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING, null=True, blank=True,
                                             related_name='payments')

    def __str__(self):
        return self.name


class PaymentFile(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, related_name='files')
    file = models.FileField(upload_to='files_record/payment_files/')

    def __str__(self):
        return f"File for {self.payment.name}"


class Student(models.Model):
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name='students')
    name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=20, unique=True)

    def clean(self):
        if not self.national_id.isdigit():
            raise ValidationError("National ID must contain only digits.")

    def __str__(self):
        return self.name


class Teacher(models.Model):
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name='teachers')
    name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=20, unique=True)

    def clean(self):
        if not self.national_id.isdigit():
            raise ValidationError("National ID must contain only digits.")

    def __str__(self):
        return self.name


class Olympiad(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, related_name='products')

    def __str__(self):
        return self.title


class Course(models.Model):
    related_product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    session_time = models.TimeField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, related_name='courses')
    students = models.ManyToManyField(Student, through='StudentAgreement')
    olympiad = models.ForeignKey(Olympiad, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='courses')

    def __str__(self):
        return self.title


class StudentAgreement(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    agreement_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    attrs = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.name} - {self.course.title}"


class TeacherAgreement(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    agreement_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    attrs = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.teacher.name} - {self.product.title}"


class PaymentAgreement(models.Model):
    PAYMENT_DIRECTION_CHOICES = [
        ('in', 'In'),
        ('out', 'Out'),
    ]

    student_agreement = models.OneToOneField(
        'StudentAgreement',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='payment_agreement'
    )
    teacher_agreement = models.OneToOneField(
        'TeacherAgreement',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='payment_agreement'
    )
    payment_direction = models.CharField(
        max_length=3,
        choices=PAYMENT_DIRECTION_CHOICES,
        default='in'
    )
    total_amount = models.IntegerField()

    def __str__(self):
        if self.student_agreement:
            return f"Payment Agreement for Student Agreement: {self.student_agreement.id}"
        elif self.teacher_agreement:
            return f"Payment Agreement for Teacher Agreement: {self.teacher_agreement.id}"
        return "Payment Agreement (No Agreement Linked)"


class Installment(models.Model):
    payment_agreement = models.ForeignKey(
        'PaymentAgreement',
        on_delete=models.CASCADE,
        related_name='installments'
    )
    amount = models.FloatField()
    due_date = models.DateTimeField()
    received_date = models.DateTimeField(null=True, blank=True)
    status = models.ForeignKey(
        'InstallmentStatus',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='installments'
    )

    def __str__(self):
        return f"Installment {self.id} for Payment Agreement {self.payment_agreement.id}"


class InstallmentStatus(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
