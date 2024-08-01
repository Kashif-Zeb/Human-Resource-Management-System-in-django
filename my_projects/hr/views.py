from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets

from .tasks import file
from .serializers import attendence_serializer, benefit_serializer, benefit_serializer_with_employeetowork, department_serializer, document_serializer, employee_serializer, employee_serializer_create, employee_serializer_for_update, get_documentserializer, get_job_serializer,job_serializer, login_serializer, payroll_serializer, performance_serializer, training_serializer, update_attendence, update_job_serializer, updates_document, user_serializer
from .models import Benefit, Department, Document,Job,Employee,Attendence, Payroll, Performance, Training, Users
# from rest_framework.mixins import CreateModelMixin,UpdateModelMixin,ListModelMixin,DestroyModelMixin,RetrieveModelMixin
# from rest_framework.generics import CreateAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateAPIView,RetrieveDestroyAPIView,RetrieveUpdateDestroyAPIView
from rest_framework  import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view,authentication_classes,permission_classes,throttle_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication,JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# Create your views here.
from functools import wraps
class custom_pagination(PageNumberPagination):
    page_size_query_param = "per_page"
    page_query_param = "page"
    max_page_size = 100

def get_user_role(request):
    auth = JWTAuthentication()
    header  = request.headers.get("Authorization")
    if header is None:
        return None
    try:
        raw_token = header.split(" ")[-1]
        validated_token = auth.get_validated_token(raw_token)
        return validated_token.get("role",None)
    except (InvalidToken, TokenError, IndexError):
        return None

def checks_roles(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def checkingrole(request,*args,**kwargs):
            breakpoint()
            role = get_user_role(request)
            if role in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                raise JsonResponse({'detail': 'You do not have permission to access this resource.'}, status=403)
        return checkingrole
    return decorator

def higherrole(view_func):
    return checks_roles(allowed_roles=["CEO","Director","CIO","CTO","HR"])(view_func)
def lowrole(view_func):
    return checks_roles(allowed_roles=["Employee"])(view_func)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = department_serializer


class create_job_with_create_mixin(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = job_serializer
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class get_job_by_id(mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset = Department.objects.all()
    serializer_class = get_job_serializer

    def get(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        job_id = serializer.validated_data['job_id']
        job = get_object_or_404(Job, job_id=job_id)
        job_serializers = job_serializer(job)
        return Response(job_serializers.data, status=status.HTTP_200_OK)

class JobListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = job_serializer
    authentication_classes = [JWTTokenUserAuthentication]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class job_update(mixins.UpdateModelMixin,generics.GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = update_job_serializer

    def put(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        job_id = serializer.validated_data['job_id']
        try:
            check_job = Job.objects.get(job_id=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer_of_job = update_job_serializer(check_job,data=request.data,partial=False)
        serializer_of_job.is_valid(raise_exception=True)
        serializer_of_job.save()
        return Response(serializer_of_job.data,status=status.HTTP_200_OK) 
    def patch(self,request,*args,**kwargs):
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        job_id = serializer.validated_data["job_id"]
        try:
            check_job = Job.objects.get(job_id =job_id)
        except:
            return Response(f"job_id {job_id}not found",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serializer_of_job = update_job_serializer(check_job,data=request.data,partial=True)
        serializer_of_job.is_valid(raise_exception=True)
        serializer_of_job.save()
        return Response(serializer_of_job.data,status=status.HTTP_200_OK)

class delete_job(mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = get_job_serializer
    authentication_classes = JWTAuthentication

    def delete(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.query_params)
        serializer.is_valid(raise_exception=True)
        job_id = serializer.validated_data["job_id"]
        try:
            check_job = Job.objects.get(job_id=job_id)
        except Job.DoesNotExist as e:
            return Response(str(e),status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.perform_destroy(check_job)
        return Response(f"the job_id {job_id} is deleted sucessfully",status=status.HTTP_200_OK)

class create_employee_and_getall(generics.ListCreateAPIView):
    queryset  = Employee.objects.all()
    pagination_class = custom_pagination
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return employee_serializer_create
        return employee_serializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)


class employeeRDU(generics.RetrieveUpdateDestroyAPIView):
    queryset  = Employee.objects.all()
    serializer_class = employee_serializer_for_update

    def get_object(self):
        """
        Override get_object to use employee_id from the request data.
        """
        employee_id = self.request.data.get('employee_id')  # Retrieve employee_id from the request body
        if not employee_id:
            raise NotFound("Employee ID not provided")

        try:
            return Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            raise NotFound("Employee not found")
    def get(self,request,*args,**kwargs):
        try:
            if "employee_id" not in request.query_params:
                raise Exception("employee_id is required")
            queryset = self.get_queryset
            emp_id  = request.query_params.get("employee_id")
            try:
                obj = Employee.objects.get(employee_id = emp_id)
            except Employee.DoesNotExist:
                raise Exception(f"employee_id {emp_id} not found")
            serializer = employee_serializer(obj)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    def delete(self, request, *args, **kwargs):
        if "employee_id" not in request.query_params:
            raise Exception("employee_id is required")
        queryset = self.get_queryset
        emp_id  = request.query_params.get("employee_id")
        try:
            obj = Employee.objects.get(employee_id = emp_id)
        except Employee.DoesNotExist:
            raise Exception(f"employee_id {emp_id} not found")
        self.perform_destroy(obj)
        return Response(f"employee_id {emp_id} is delted successfully",status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    

class attendence_crud(APIView):
    def post(self,request):
        serializer = attendence_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self,request):
       
        if "employee_id" not in request.query_params:
            return Response ("employee_id is required",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        emp = request.query_params.get("employee_id")
        if not emp:
            return Response("employee_id can't be left empty", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if not emp.isdigit() or int(emp) <= 0:
            return Response("employee_id must be a positive integer", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
      
        emp = int(emp)
        obj = Attendence.objects.filter(employee_id=emp).order_by("-date").all()
        if not obj:
            return Response(f"employee_id {emp} not found",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serializer = attendence_serializer(obj,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request):
        serializer = update_attendence(data=request.data)
        if serializer.is_valid(raise_exception=True):
            at_id = serializer.validated_data.get("attendence_id")
            try:
                check_at = Attendence.objects.get(attendence_id=at_id)
            except:
                return Response(f"attendence_id {at_id} not found",status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            updated_Data = attendence_serializer(check_at,data=request.data,partial=True)
            if updated_Data.is_valid(raise_exception=True):
                updated_Data.save()
                return Response(updated_Data.data,status=status.HTTP_200_OK)
            else:
                return Response(updated_Data.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
             return Response(serializer.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    

    def delete(self,request):
        if "attendence_id" not in request.query_params:
            return Response("attendence_id is required",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        at_id = request.query_params.get("attendence_id")
        if not at_id:
            return Response("attendence_id cannot be left empty",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if not at_id.isdigit() or int(at_id)<=0:
            return Response("attendence_id must be a positive integer",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try:
            at_id = int(at_id)
            obj = Attendence.objects.get(attendence_id=at_id)
        except:
            return Response(f"attendence_id {at_id} not found",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        obj.delete()
        return Response(f"attendence_id {at_id} deleted_successfully",status=status.HTTP_200_OK)
    
@api_view(["POST"])
def create_document(request):
    serializer =  document_serializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED,content_type="application/json")
    return Response(serializer.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_name = validated_token.get('user_name')
        return Users.objects.filter(user_name=user_name).first()
@api_view(["GET"])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
# @higherrole
# @lowrole
def get_documents(request):
    serializer = get_documentserializer(data=request.query_params)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        if "employee_id" in data:
            obj =Document.objects.filter(employee_id=data['employee_id']).all().order_by("-document_id")
            fetched_data = document_serializer(obj,many=True)
            aaa=file.delay(fetched_data.data)
            return Response(fetched_data.data,status=status.HTTP_200_OK)
        else:
            obj = Document.objects.get(document_id=data['document_id'])
            fetched_data = document_serializer(obj)
            aaa=file.delay(fetched_data.data)
            return Response(fetched_data.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["PUT"])
def update_document(request):
    serializer = updates_document(data=request.data)
    if serializer.is_valid(raise_exception=True):
        document_id = serializer.validated_data.get("document_id")
        # Retrieve the document or return 404
        check_document = get_object_or_404(Document, document_id=document_id)
        
        # Update the document with partial data
        updated_data = document_serializer(check_document, data=request.data, partial=True)
        if updated_data.is_valid(raise_exception=True):
            updated_data.save()
            return Response(updated_data.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    # document_id = request.data.get("document_id")
    # if not document_id:
    #     return Response({"error": "document_id is required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    # document = get_object_or_404(Document, document_id=document_id)
    
    # # Use DocumentSerializer to validate and update the instance
    # serializer = document_serializer(document, data=request.data, partial=True) 
    
    # if serializer.is_valid(raise_exception=True):
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    # return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



@api_view(["DELETE"])
def delete_document(request):
    if "document_id" not in request.query_params:
        return Response("document_id is required",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    id = request.query_params.get("document_id")
    if not id :
        return Response("document_id cannot be left empty")
    if not id.isdigit() or int(id)<=0:
        return Response("document_id must be a positive integer")
    id = int(id)
    obj = Document.objects.filter(document_id=id).first()
    if obj:
        obj.delete()
        return Response(f"document_id {id} is deleted successfully",status=status.HTTP_200_OK)
    return Response(f"document_id {id} is not found",status=status.HTTP_422_UNPROCESSABLE_ENTITY)



class crud_benefit(viewsets.ModelViewSet):
    queryset = Benefit.objects.all()
    serializer_class = benefit_serializer
    # lookup_field = 'benefit_id'

class crud_employee_again_for_benefit(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = benefit_serializer_with_employeetowork
    lookup_field = 'employee_id'





class modelview_of_payroll(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = payroll_serializer

class modelview_of_training(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = training_serializer


class modelview_of_performance(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = performance_serializer



class user_registraion(generics.CreateAPIView):
    serializer_class = user_serializer
    queryset = Users.objects.all()

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


@api_view(["POST"])
def login(request):
    serializer = login_serializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        user = Users.objects.get(email=email)
        if user:
            if user.password  == password:
                refresh = RefreshToken
                refresh=  refresh.for_user(user)
                refresh["role"] = user.role
                return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
            else:
                return Response("email is invalid",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response("email is invalid",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response(serializer.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)