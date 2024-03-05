from rest_framework import serializers
from .models import User, ProjectRegistration, ProjectSubmission, Notifications, Marks
import datetime, re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','profile_pic' ,'clg_id', 'first_name', 'last_name', 'role', 'gender', 'email', 'address', 'branch', 'year', 'dob', 'mobile', 'password'] #, 'is_active', 'is_verified'] , 'profile_pic'
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

    def validate(self, data):
        if data['role'] == 'student':
            if not re.search(r'(?i)n[0-9]{6}@rguktn\.ac\.in', data['email']):
                raise serializers.ValidationError('Invalid Email')
        
        return data


# class UpdateProfileSerializer(serializers.ModelSerializer):
#     # first_name = serializers.CharField(write_only=True, required=True)
#     # last_name = serializers.CharField(write_only=True, required=True)
#     # gender = serializers.CharField(write_only=True, required=True)
#     # dob = serializers.CharField(write_only=True, required=True)
#     # mobile = serializers.CharField(write_only=True, required=True)
#     # address = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ( 'first_name', 'last_name', 'dob', 'branch', 'year', 'mobile', 'address')


#     def update(self, instance, validated_data):
#         print("---->", validated_data,"--->", instance)
#         instance.first_name=validated_data.get('first_name', instance.first_name)
#         instance.last_name=validated_data.get('last_name', instance.last_name)
#         # instance.gender=validated_data['gender']
#         instance.dob=validated_data.get('dob', instance.dob)
#         instance.mobile=validated_data.get('mobile', instance.mobile)
#         instance.branch = validated_data.get('branch', instance.branch)
#         instance.year = validated_data.get('year', instance.year)
#         instance.address=validated_data.get('address', instance.address)
#         instance.save()
        
#         return instance

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = True)
    password2 = serializers.CharField(write_only = True, required = True)
    old_password = serializers.CharField(write_only = True, required = True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password":"Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class ProjectRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRegistration
        fields = ('clg_id', 'branch', 'faculty', 'aca_year','topic')


class ProjectSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectSubmission
        fields = ('submission_date', 'faculty', 'clg_id', 'aca_year','project_id', 'project_title', 'individual_or_team', 'project_description', 'project_file')

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        details = list(ProjectRegistration.objects.filter(clg_id = validated_data['clg_id'], is_submitted = 0).values_list('faculty', 'aca_year'))[0]
        instance.faculty = details[0]
        instance.aca_year = details[1]
        instance.submission_date = datetime.date.today()

        instance.save()

        return instance

class NotificationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = ('is_viewed','clg_id','due_date','msg_title','instructions', 'faculty')

class MarksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marks
        fields = ('clg_id', 'faculty', 'project_id','design_marks', 'working_marks', 'comments')

    # def create(self, validated_data):
    #     instance = self.Meta.model(**validated_data)
