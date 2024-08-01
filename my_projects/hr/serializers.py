from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import Attendence, Benefit, Department, Document, Job,Employee, Payroll, Performance, Training, Users
from .validators import validations as v
class department_serializer(serializers.ModelSerializer):
    # CustomerID = serializers.IntegerField(dump_only=True,)
    class Meta:
        model  = Department
        fields = "__all__"
        # read_only_fields

class job_serializer(serializers.Serializer):
    job_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True,max_length=50,validators=[v.no_space("name")])
    description = serializers.CharField(max_length = 200,validators=[v.no_space("description")])
    salary_range = serializers.DictField(child=serializers.IntegerField(),required=True)
    def validate_salary_range(self, value):
        if not isinstance(value, dict) or 'minimum' not in value or 'maximum' not in value:
            raise serializers.ValidationError("salary_range must be a dictionary with 'minimum' and 'maximum' keys.")
        if value['minimum'] < 1 or value['maximum'] > 9999999999:
            raise serializers.ValidationError("Values for 'minimum' and 'maximum' must be between 1 and 9999999999.")
        if value['minimum'] > value['maximum']:
            raise serializers.ValidationError("'minimum' cannot be greater than 'maximum'.")
        return value
    def create(self, validated_data):
        # salary_range = validated_data.pop('salary_range')
        return Job.objects.create(**validated_data)

class get_job_serializer(serializers.Serializer):
    job_id = serializers.IntegerField(required=True)


class update_job_serializer(serializers.ModelSerializer):
    job_id = serializers.IntegerField(required=True)
    class Meta:
        model = Job
        fields = "__all__"

class employee_serializer_create(serializers.ModelSerializer):
    # job_id = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    # department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    class Meta:
        model  = Employee
        fields = ['employee_id', 'name', 'address', 'phone', 'email',"job_id","department_id"]


class employee_serializer(serializers.ModelSerializer):
    job = job_serializer(source ="job_id")
    department = department_serializer(source="department_id")
    class Meta:
        model  = Employee
        fields = ['employee_id', 'name', 'address', 'phone', 'email', 'job', 'department']
        # exclude = ["jod_id","department_id"]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Renaming fields
        job_details = representation.get('job')
        if job_details:
            job_details.pop('job_id')

        department_details = representation.get('department')
        if department_details:
            department_details.pop('department_id')
        return representation
    
class employee_serializer_for_update(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        extra_kwargs = {'employee_id': {'required': True}}
    # def update(self, instance, validated_data):
    #     employee_id = validated_data.get('employee_id', None)

    #     if employee_id and not Employee.objects.filter(employee_id=employee_id).exists():
    #         raise ValidationError({'employee_id': 'This employee does not exist.'})

    #     return super().update(instance, validated_data)

class attendence_serializer(serializers.ModelSerializer):
    class Meta:
        model = Attendence
        fields = "__all__"

class update_attendence(attendence_serializer):
    attendence_id = serializers.IntegerField(required=True)

class document_serializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"

class updates_document(document_serializer):
    document_id = serializers.IntegerField(required=True)


class get_documentserializer(serializers.Serializer):
    employee_id = serializers.IntegerField(required=False)
    document_id = serializers.IntegerField(required=False)

    def validate(self, data):
        if not ('employee_id' in data or 'document_id' in data):
            raise serializers.ValidationError("Either employee_id or document_id must be provided.")
        if 'employee_id' in data and 'document_id' in data:
            raise serializers.ValidationError("Only one of employee_id or document_id must be provided.")
        return data

class benefit_serializer(serializers.HyperlinkedModelSerializer):
    employee_id = serializers.HyperlinkedRelatedField(
        view_name='employee-detail',  # Name of the view that handles the Employee details
        queryset=Employee.objects.all(),
        lookup_field = 'employee_id'
    )

    class Meta:
        model = Benefit
        fields = ['url', 'benefit_id', 'benefit_type', 'description', 'start_date', 'end_date', 'employee_id']
        # extra_kwargs = {
        #     'url': {'view_name': 'benefit-detail'}
        # }

class benefit_serializer_with_employeetowork(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ['url', 'employee_id', 'name', 'address', 'phone', 'email', 'job_id', 'department_id']
        # extra_kwargs = {
        #     'url': {'view_name': 'employee-detail'}
        # }


class payroll_serializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = "__all__"
        

class performance_serializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = "__all__"


class training_serializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = "__all__"

roles = ["CEO","Director","Employee","CIO","CTO","HR"]

class user_serializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=roles)
    class Meta:
        model = Users
        fields = "__all__"

class login_serializer(serializers.Serializer):
    email = serializers.EmailField(required=True,max_length=200)
    password = serializers.CharField(required=True,max_length=50)