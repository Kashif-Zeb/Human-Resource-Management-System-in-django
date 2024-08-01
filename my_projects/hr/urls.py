from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views 
router = DefaultRouter()
router.register(prefix='dept', viewset=views.DepartmentViewSet, basename='department')
router.register(prefix="benefits", viewset=views.crud_benefit, basename="benefit")
router.register(prefix="employees", viewset=views.crud_employee_again_for_benefit, basename="employee")
router.register(prefix="payrolls", viewset=views.modelview_of_payroll, basename="payroll")
router.register(prefix="performances", viewset=views.modelview_of_performance, basename="performance")
router.register(prefix="trainings", viewset=views.modelview_of_training, basename="training")
# router.register(prefix="jobs", viewset=views.crud_job_again_for_benefit, basename="job")
urlpatterns = [
    path('', include(router.urls)),
    path("registration/",views.user_registraion.as_view(),name="registrations"),
    path("login/",views.login,name="login"),
    path("create_job/",views.create_job_with_create_mixin.as_view(),name="create job"),
    path("get_job/",views.get_job_by_id.as_view(),name="get job by id"),
    path("get_all_job/",views.JobListView.as_view(),name="get all id"),
    path("update_job/",views.job_update.as_view(),name="update job"),
    path("delete_job/",views.delete_job.as_view(),name="delete job"),
    path("employeeCGA/",views.create_employee_and_getall.as_view(),name="get all employee and create employee"),
    path("employeeDRU/",views.employeeRDU.as_view(),name="employee get update delete"),
    path("attendence/",views.attendence_crud.as_view(),name="attendence crud"),
    path("create_document/",views.create_document,name="creating document"),
    path("get_document/",views.get_documents,name="geting document"),
    path("update_document/",views.update_document,name="updating document"),
    path("delete_document/",views.delete_document,name="delete_document document")
]
