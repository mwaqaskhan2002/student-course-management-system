from django.db.models import Q
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import StudentForm, DepartmentForm, CourseForm
from .models import Course, Student, Department
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse


class HomeView(TemplateView):
    template_name = 'students/home.html'

class StudentCreateView(SuccessMessageMixin, CreateView):
    model = Student  #Database
    form_class = StudentForm    #Form Style
    template_name = 'students/student_form.html' #HTML template
    success_url = reverse_lazy('students:student_list') #redirect page to student list 
    success_message = "Student '%(name)s' added successfully!" #Success message with dynamic student name
    
class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students' #students ke naam se template me access karenge student objects ko
    
    def get_queryset(self):
        
        queryset = super().get_queryset().select_related('department').prefetch_related('courses')
        
        #Department Filter and Sorting Parameters
        search_query = self.request.GET.get('search')
        selected_dept = self.request.GET.get('department')
        order_by = self.request.GET.get('order_by', 'newest')
        
        # 1. SEARCH FILTER LOGIC (Gives results if matches Name OR Email)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(email__icontains=search_query) |
                Q(department__department_name__icontains=search_query) |
                Q(department__department_code__icontains=search_query) | 
                Q(courses__course_code__icontains=search_query)
            ).distinct()
        
        #Department Filter
        if selected_dept and selected_dept != 'all':
            queryset = queryset.filter(department_id=selected_dept)
        
        #Sorting Filter
        if order_by == "name_asc":
            queryset = queryset.order_by('name')
        elif order_by == 'newest':
            return queryset.order_by('-id')
        elif order_by == "name_desc":
            queryset = queryset.order_by('-name')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #To send all department to appear in the dropdown
        context['departments'] = Department.objects.all()
        return context
    
class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student' #student ke naam se template me access karenge specific student object ko

class StudentUpdateView(SuccessMessageMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html' 
    success_url = reverse_lazy('students:student_list')
    success_message = "Student '%(name)s' details updated successfully!"

class StudentDeletePermanentView(SuccessMessageMixin, DeleteView):
    model = Student 
    success_url = reverse_lazy('students:student_list')
    success_message = "Student record deleted permanently!"
    
    def form_valid(self,form):
        success_url = self.get_success_url()
        student = self.get_object()
        student.delete()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(success_url)
    
class StudentRemoveFromDepartmentView(SuccessMessageMixin, DeleteView):
    model = Student 
    success_url = reverse_lazy('students:student_list')
    success_message = "Student removed from department"
    
    def form_valid(self,form):
        student = self.get_object()
        department = student.department
        
        if student.department:
            student.courses.clear()
            
            student.department = None
            student.save()
            
            messages.success(
                self.request, 
                f"Successfully removed {student.name} from department and un-enrolled from all its courses."
            )
        if department:
            messages.success(
                self.request, 
                f"Successfully removed {student.name} from {department.department_name} and un-enrolled from all its courses."
            )
            return HttpResponseRedirect(reverse_lazy('students:department_detail', kwargs={'pk': department.pk}))
        return HttpResponseRedirect(self.success_url)
    
class DepartmentListView(ListView):
    model = Department
    template_name = 'students/department_list.html'
    context_object_name = 'departments'
    
    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('courses')       
        
        # URL Parameters
        search_query = self.request.GET.get('search')
        order_by = self.request.GET.get('order_by', 'newest')
        
        # Department Name or Department Code 
        if search_query:
            queryset = queryset.filter(
                Q(department_name__icontains=search_query) | 
                Q(department_code__icontains=search_query) |
                Q(courses__course_code__icontains=search_query)
            ).distinct()
        
        # Sorting Logic
        if order_by == 'name_asc':
            queryset = queryset.order_by('department_name')   
        elif order_by == 'name_desc':
            queryset = queryset.order_by('-department_name')   
        elif order_by == 'code_asc':
            queryset = queryset.order_by('department_code')   
        elif order_by == 'newest':
            queryset = queryset.order_by('-id')           
        return queryset
    
class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'students/department_detail.html'
    context_object_name = 'department'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = self.object.students.all()
        return context
    
    
def ajax_get_courses(request):
    department_id = request.GET.get('department_id')
    
    if department_id:
        courses = Course.objects.filter(department_id=department_id)
    else:
        courses = Course.objects.all()
        
    courses_data = [
        {
            'id': course.id, 
            'course_name': course.course_name, 
            'course_code': course.course_code
        } 
        for course in courses
    ]
    return JsonResponse({'courses': courses_data})

def load_courses(request):
    department_id = request.GET.get('department_id')
    courses = Course.objects.filter(departments__id=department_id).values('id', 'course_name', 'course_code')
    return JsonResponse(list(courses), safe=False)

class DepartmentCreateView(SuccessMessageMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'students/department_form.html' # Dono ke liye common ya alag template rakh sakte hain
    success_url = reverse_lazy('students:department_list')
    success_message = "Department created successfully!"
    
class DepartmentUpdateView(SuccessMessageMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'students/department_form.html'
    success_url =  reverse_lazy('students:department_list')
    # success_message = "Department '%(name)s'  updated successfully!"
    
class DepartmentDeleteView(SuccessMessageMixin, DeleteView):
    model = Department
    success_url = reverse_lazy('students:department_list')
    success_message = "Department and all its associated courses deleted successfully!"

    def form_valid(self, form):
        success_url = self.get_success_url()
        department = self.get_object()
        
        for course in department.courses.all():
            if course.departments.count() > 1:
                course.departments.remove(department)
            else:
                course.delete()
        department.delete()
        
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(success_url)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CourseListView(ListView):
    model = Course
    form_class = CourseForm
    template_name = 'students/course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('departments')
        
        # URL parameters 
        search_query = self.request.GET.get('search')
        selected_dept = self.request.GET.get('department')
        order_by = self.request.GET.get('order_by', 'newest')
        
        # Department Name or Department Code
        if search_query:
            queryset = queryset.filter(
                Q(course_name__icontains=search_query) | 
                Q(course_code__icontains=search_query)
            ).distinct()
        
        # Department Filter
        if selected_dept and selected_dept != 'all':
            queryset = queryset.filter(departments__id=selected_dept)
        
        # Sorting Logic
        if order_by == 'name_asc':
            queryset = queryset.order_by('course_name')   
        elif order_by == 'code_asc':
            queryset = queryset.order_by('course_code')   
        elif order_by == 'newest':
            queryset = queryset.order_by('-id')           
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()  
        return context

class CourseCreateView(SuccessMessageMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'students/course_form.html'
    success_url = reverse_lazy('students:course_list') 
    success_message = "Course created successfully!"
    
class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'students/course_form.html'  
    success_url = reverse_lazy('students:course_list')

class CourseDeleteView(SuccessMessageMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('students:course_list')
    success_message = "Course deleted successfully!"
    
    def form_valid(self, form):
        success_url = self.get_success_url()
        course = self.get_object()
        course.delete()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(success_url)
    
    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return self.delete(request, *args, **kwargs)
    