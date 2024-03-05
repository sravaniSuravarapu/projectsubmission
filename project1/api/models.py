from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import FileExtensionValidator
from django.forms import CharField, IntegerField

# from project1.project1.settings import DEFAULT_AUTO_FIELD
# from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password, first_name='',last_name='',gender='',mobile='', dob='', address='', **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_verified', True)
        user = self.model( email=email,first_name=first_name,last_name=last_name,gender=gender, mobile=mobile, dob=dob,address=address, **extra_fields)
        #user.save()
        user.set_password(password)
        user.save()
        print("-->",user)
        return user

    def create_superuser(self, email, password, first_name='',last_name='', **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user( email, password, first_name,last_name, **extra_fields)


class User(AbstractUser):
    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
    id = models.BigAutoField( primary_key=True, default=1)
    profile_pic = models.ImageField(default='default.jpg', upload_to="images/", null=True, blank = True)
    clg_id = models.CharField(max_length=7, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=10)
    gender = models.CharField(max_length=6)
    email = models.CharField(max_length=255, unique=True,db_index=True)
    address = models.CharField(max_length=255, blank=True)
    dob = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    year = models.CharField(max_length=10, null=True, blank=True)
    mobile = models.CharField(max_length=13)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True) #change default to False after smtp is possible

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    # def save(self):
    #     super().save()

    #     img = Image.open(self.profile_pic.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_pic.path)

    # def save(self, *args, **kwargs):
	#     super(User, self).save(*args, **kwargs)

class ProjectRegistration(models.Model):
    # email = models.EmailField(max_length=255, unique=True,db_index=True)
    clg_id = models.CharField(max_length=7)
    branch = models.CharField(max_length=5)
    faculty = models.CharField(max_length=30)
    aca_year = models.CharField(max_length=10)
    topic = models.CharField(max_length=30)
    is_submitted = models.IntegerField(default=0)


class ProjectSubmission(models.Model):
    submission_date = models.DateField(null=True, blank=True)
    faculty = models.CharField(max_length= 50, null=True, blank=True)
    clg_id = models.CharField(max_length=7)
    aca_year = models.CharField(max_length=10, null=True, blank=True) 
    project_id = models.CharField(max_length=20)
    project_title = models.CharField(max_length=30)
    individual_or_team = models.CharField(max_length=15)
    project_description = models.CharField(max_length=150)
    project_file = models.FileField(upload_to="project_files", null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['zip'])])
    is_marked = models.IntegerField(default=0)

    def __str__(self):
        return self.project_title

class Notifications(models.Model):
    is_viewed = models.IntegerField(default=0)
    clg_id = models.CharField(max_length=7, null=True, blank=True)
    due_date = models.CharField(max_length=20)
    msg_title = models.CharField(max_length=30)
    instructions = models.CharField(max_length=200)
    faculty = models.CharField(max_length=50)

    def __str__(self):
        return self.clg_id

class Marks(models.Model):
    clg_id = models.CharField(max_length=7)
    faculty = models.CharField(max_length=50, blank=True, null=True)
    project_id = models.CharField(max_length=20)
    design_marks = models.IntegerField()
    working_marks = models.IntegerField()
    comments = models.CharField(max_length=100, blank= True, null= True)
