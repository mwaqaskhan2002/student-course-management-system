from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


# ============================
# VALIDATORS 
# ============================
text_only_validator = RegexValidator(
    regex=r"^[a-zA-Z\s]+$",
    message="Invalid entry! Only alphabets and spaces are allowed."
)

code_validator = RegexValidator(
    regex=r"^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]+$",
    message="Invalid Code! Code must contain a mix of BOTH alphabets and numbers (e.g., CS101, MGT101), with no spaces or special characters."
)

digits_only_validator = RegexValidator(
    regex=r'^\d+$', 
    message="Invalid phone number. It must contain digits only."
)

# ============================
# MODELS
# ============================

class Student(models.Model):
    name = models.CharField(null=False, max_length=100, validators=[text_only_validator])
    
    age = models.IntegerField(null=False,
            validators=[MinValueValidator(18, message="Age Must be at least 18"), 
            MaxValueValidator(90, message="Age must be less than 90")]
        )
    
    email = models.EmailField(unique=True)
    
    phone_number = models.CharField(
        max_length=11, 
        unique=True, 
        validators=[
            digits_only_validator,
            RegexValidator(
                regex=r'^03\d{9}$', 
                message="Invalid phone number! It must be exactly 11 digits long, start with '03', and contain numbers only."
            ),
        ]
    )

    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    courses = models.ManyToManyField('Course', blank=True, related_name='students')

    def __str__(self):
        return self.name
    
    
class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True, validators=[text_only_validator])
    department_code = models.CharField(max_length=8, unique=True, validators=[text_only_validator])
    

    def __str__(self):
        return self.department_name
    
    def save(self, *args, **kwargs):
        if self.department_code:
            self.department_code = self.department_code.upper()
        super().save(*args, **kwargs)
    
    
class Course(models.Model):
    course_name = models.CharField(max_length=100, validators=[text_only_validator])
    course_code = models.CharField(max_length=8, validators=[code_validator])
    departments = models.ManyToManyField(Department, blank=True, related_name='courses')
    
    def __str__(self):
        return f"{self.course_name} ({self.course_code})"
    
    def save(self, *args, **kwargs):
        if self.course_code:
            self.course_code = self.course_code.upper()
        super().save(*args, **kwargs)