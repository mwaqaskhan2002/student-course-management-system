from . import views
from django.urls import include, path
from .views import StudentCreateView, StudentListView, StudentDetailView, StudentUpdateView, StudentDeletePermanentView, StudentRemoveFromDepartmentView, DepartmentListView, DepartmentDetailView, HomeView
from django.views.generic import TemplateView

app_name = 'students'

urlpatterns = [
    path('', StudentListView.as_view(), name='student_list'),
    path('add/', StudentCreateView.as_view(), name='student_create'),
    path('detail/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('edit/<int:pk>/', StudentUpdateView.as_view(), name='student_edit'),
    path('student/<int:pk>/remove-dept/', views.StudentRemoveFromDepartmentView.as_view(), name='student_remove_dept'),
    path('student/<int:pk>/delete/', views.StudentDeletePermanentView.as_view(), name='student_delete_permanent'),
    
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('department/add/', views.DepartmentCreateView.as_view(), name='department_add'),
    path('department/edit/<int:pk>/', views.DepartmentUpdateView.as_view(), name = 'department_edit'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department_detail'),
    path('department/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),
    path('ajax/get-courses/', views.ajax_get_courses, name='ajax_get_courses'),
    path('ajax/load-courses/', views.load_courses, name='ajax_load_courses'),
    
    
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('course/add/', views.CourseCreateView.as_view(), name='course_add'),
    path('course/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_update'),
    path('course/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
]
