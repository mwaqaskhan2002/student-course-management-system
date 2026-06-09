import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Student, Department, Course


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'email', 'phone_number', 'department', 'courses']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter age','inputmode': 'numeric','pattern': '[0-9]*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            
            'department': forms.Select(attrs={'class': 'form-select'}),
            'courses': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
        
        error_messages = {
            'name': {
                'invalid': 'Invalid entry. Please enter name in text.',
                'required': 'Please enter your name.',
            },
            'age': {
                'invalid': 'Invalid entry. Please enter age in numbers.',
                'required': 'Please enter age.',
            },
            'email': {
                'invalid': 'Please enter a valid email address.',
                'required': 'Please enter email address.',
            },
            'phone_number': {
                'invalid': 'Please enter a valid phone number.',
                'required': 'Please enter phone number.',
            },
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        if self.data and 'department' in self.data:
            
            try:
                department_id = int(self.data.get('department'))
                self.fields['courses'].queryset = Course.objects.filter(departments__id=department_id)
            except (ValueError, TypeError):
                self.fields['courses'].queryset = Course.objects.none()
                
        elif self.instance and self.instance.pk and self.instance.department:
            self.fields['courses'].queryset = Course.objects.filter(departments=self.instance.department)
        else:
            self.fields['courses'].queryset = Course.objects.none()

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'department_code']
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Computer Science'}),
            'department_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CS'}),
        }
        
    def clean_department_name(self):
        department_name = self.cleaned_data.get('department_name')
        if department_name:
            if not re.match(r"^[a-zA-Z\s]+$", department_name):
                raise ValidationError("Invalid entry. Department name must contain alphabets and spaces only.")
            
            queryset = Department.objects.filter(department_name__iexact=department_name)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise ValidationError("A department with this name already exists.")
        return department_name 
    
    def clean_department_code(self):
        department_code = self.cleaned_data.get('department_code')
        if department_code:
            if not re.match(r"^[a-zA-Z]+$", department_code):
                raise ValidationError("Invalid entry. Department code must contain alphabets only (e.g., CS, AF, BBA).")

            department_code_upper = department_code.upper()
            queryset = Department.objects.filter(department_code__iexact=department_code_upper)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise ValidationError("A department with this code already exists.")
                
        return department_code
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_code', 'departments']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduction to Programming'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CS101'}),
            'departments': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
        
    def clean_course_name(self):
        course_name = self.cleaned_data.get('course_name')
        if course_name:
            if not re.match(r"^[a-zA-Z\s]+$", course_name):
                raise ValidationError("Invalid entry. Course name must contain alphabets and spaces only.")
        return course_name
    
    def clean_course_code(self):
        course_code = self.cleaned_data.get('course_code')
        if course_code:
            if not re.match(r"^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]+$", course_code):
                raise ValidationError("Course code must contain both letters and numbers (e.g., CS101, MGT101).")
            return course_code.upper()
        return course_code

    def clean(self):
        cleaned_data = super().clean()
        course_code = cleaned_data.get("course_code")
        selected_departments = cleaned_data.get("departments")
        
        if course_code and selected_departments:
            course_code_upper = course_code.upper()
            
            for dept in selected_departments:
                queryset = Course.objects.filter(course_code=course_code_upper, departments=dept)
                if self.instance.pk:
                    queryset = queryset.exclude(pk=self.instance.pk)
                if queryset.exists():
                    raise ValidationError(
                        f"The course code '{course_code_upper}' already exists under the '{dept.department_name}' department."
                    )
        return cleaned_data