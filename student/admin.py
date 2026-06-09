from os import name
from django.forms import CheckboxSelectMultiple
from django.contrib import admin
from django.db import models
from .models import Department, Student, Course

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'email', 'get_department_name','phone_number')
    search_fields = ('name', 'email', 'department__department_name')
    list_filter = ('age', 'department')
    ordering = ('name',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('department')
    
    @admin.display(ordering='department__department_name', description='Department')
    def get_department_name(self, obj):
        return obj.department.department_name if obj.department else "None"
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'department_code', 'display_course_codes')
    search_fields = ('department_name', 'department_code', 'display_course_codes')
    ordering = ('department_name',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('courses')
    
    def display_course_codes(self, obj):
        return ", ".join([course.course_code for course in obj.courses.all()])
    display_course_codes.short_description = 'Course Codes'
    
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_code', 'display_departments')
    search_fields = ('course_name', 'course_code', 'departments__department_name')
    list_filter = ('departments',)
    ordering = ('course_name',)
    
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('departments')
    
    def display_departments(self, obj):
        return ", ".join([dept.department_name for dept in obj.departments.all()])
    display_departments.short_description = 'Departments'
    