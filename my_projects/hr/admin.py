from django.contrib import admin
from .models import Department,Job,Attendence,Document,Employee,Payroll,Performance,Benefit,Training, Users
# Register your models here.
@admin.register(Department)
class Department_page(admin.ModelAdmin):
    list_display =[ "department_id" ,
    "name" ]
@admin.register(Job)
class Job_page(admin.ModelAdmin):
    
    list_display =["job_id" ,
    "name" ,
    "description" ,
    "salary_range" ]


@admin.register(Employee)
class Employee_page(admin.ModelAdmin):
    list_display = ["employee_id" ,
    "name" ,
    "address"  ,
    "phone" ,
    "email" ,
    "job_id" ,
    "department_id"  ]

@admin.register(Payroll)
class Payroll_page(admin.ModelAdmin):
    list_display = ["payroll_id" ,
    "salary",
    "bonus",
    "deduction" ,
    "paydate" ,
    "employee_id" ]
@admin.register(Performance)
class Performance_page(admin.ModelAdmin):
    list_display = ["performance_id"  ,
    "reviewdate" ,
    "score" ,
    "feedback" ,
    "employee_id" ]
@admin.register(Benefit)
class Benefit_page(admin.ModelAdmin):
    list_display = ["benefit_id" ,
    "benefit_type" ,
    "description" ,
    "start_date" ,
    "end_date" ,
    "employee_id" ]

@admin.register(Document)
class Document_page(admin.ModelAdmin):
    list_display =["document_id"  ,
    "document_type" ,
    "file_path" ,
    "employee_id" ]

@admin.register(Attendence)
class Attendence_page(admin.ModelAdmin):
    list_display = ["attendence_id" ,
    "date" ,
    "check_in_time" ,
    "check_out_time" ,
    "employee_id" ]

@admin.register(Training)
class Training_page(admin.ModelAdmin):
    list_display = ["training_id",
    "training_name" ,
    "date" ,
    "status" ,
    "description",
    "get_employees" ]

    def get_employees(self, obj):
        return ", ".join([employee.name for employee in obj.employees.all()])
    get_employees.short_description = 'Employees'


@admin.register(Users)
class User_page(admin.ModelAdmin):
    list_display = ["user_id",
    "user_name" ,
    "email" ,
    "password" ,
    "role"]