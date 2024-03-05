from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from .serializers import ProjectRegistrationSerializer, ProjectSubmissionSerializer, NotificationsSerializer, MarksSerializer
from .models import User, ProjectRegistration, ProjectSubmission, Notifications, Marks
# from .mails import send_verify_mail, send_password_mail
from project1.settings import key, MEDIA_ROOT
from django.http import FileResponse
from django.contrib import messages
import jwt
from .logs import logger


def display_dashboard(request):
    token = request.COOKIES.get('token', None)

    if token==None:
        logger.error("Token not exist")
        return redirect("login-page")

    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
        print(payload)
    except jwt.ExpiredSignatureError:
        return redirect("login-page")

    user = User.objects.filter(email=payload['email']).first()

    if payload['role'] == 'student':

        faculty = User.objects.filter(role = 'faculty', branch = user.branch).all()
        avail_faculty = []

        for i in list(faculty.values()):
            faculty_name = i['first_name'] + " " + i['last_name']
            count = ProjectRegistration.objects.filter(faculty = faculty_name).count()
            if count < 30:
                avail_faculty.append(faculty_name)

        projects = ProjectSubmission.objects.filter(clg_id = user.clg_id).all()
        notifications = Notifications.objects.filter(clg_id = user.clg_id).all()

        return render(request, 'project1/student-dashboard.html', {'user':user, 'faculty':avail_faculty, 'projects':projects, 'notifications':notifications})


    elif payload['role'] == 'faculty':

        faculty_name = user.first_name + " " + user.last_name
        registered = ProjectRegistration.objects.filter(faculty = faculty_name).all()
        submitted = ProjectSubmission.objects.filter(faculty = faculty_name).all()
        submitted_list = list(submitted.values())
        registered_list = list(registered.values())
        
        rcountDict = {
            'Puc1' : 0,
            'Puc2' : 0,
            'E1' : 0,
            'E2' : 0,
            'E3' : 0,
            'E4' : 0
        }

        scountDict = {
            'Puc1' : 0,
            'Puc2' : 0,
            'E1' : 0,
            'E2' : 0,
            'E3' : 0,
            'E4' : 0
        }

        for j in registered_list:
            student = User.objects.filter(clg_id = j['clg_id']).first()
            j.update({'name': student.first_name + ' ' + student.last_name })
            rcountDict[j['aca_year']] += 1

        rCountList = list(rcountDict.values())
            

        for i in submitted_list:
            student = User.objects.filter(clg_id = i['clg_id']).first()
            i.update({'branch': student.branch, 'name': student.first_name + ' ' + student.last_name})
            scountDict[i['aca_year']] += 1
        
        sCountList = list(scountDict.values())

        overAllStats = [submitted.count(), (registered.count() - submitted.count())]

        return render(request, 'project1/faculty-dashboard.html', {'user':user, 'registered':registered_list, 'submitted':submitted_list, 'rCountList':rCountList, 'sCountList':sCountList, 'overAllStats':overAllStats})

def display_scoreboard(request):
    token = request.COOKIES.get('token', None)

    if token==None:
        logger.error("Token not exist")
        return redirect("login-page")

    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
        print(payload)
    except jwt.ExpiredSignatureError:
        return redirect("login-page")

    user = User.objects.filter(email=payload['email']).first()

    if payload['role'] == 'student':
        projects = ProjectSubmission.objects.filter(clg_id = user.clg_id, is_marked = 1).all()
        projects = list(projects.values())

        for i in projects:
            print(i['project_id'])
            marks = Marks.objects.filter(project_id = i['project_id']).first()
            score = (marks.design_marks + marks.working_marks) / 2
            i.update({'design_marks': marks.design_marks, 'working_marks':marks.working_marks, 'score':score,'comments':marks.comments})

        print('\n\n--->', projects)

        return render(request, 'project1/student_scoreboard.html', {'user':user, 'majorProjects':projects})
    elif payload['role'] == 'faculty':

        faculty_name = user.first_name + " " + user.last_name
        projects = list(ProjectSubmission.objects.filter(faculty = faculty_name).all().values())

        for i in projects:
            students  = User.objects.filter(clg_id = i['clg_id']).first()
            i.update({'name': students.first_name + " " + students.last_name})

        return render(request, 'project1/Faculty_scoreboard.html', {'user':user, 'projects':projects})


def display_about(request):
    return render(request, 'project1/about.html')


#student apis

def register_project(request):
    serializer = ProjectRegistrationSerializer(data=request.POST)

    user = ProjectRegistration.objects.filter(clg_id = request.POST.get('clg_id')).first()

    if user is not None:

        not_submitted = ProjectRegistration.objects.filter(clg_id = request.POST.get('clg_id'), is_submitted = 0).exists()

        if not_submitted:
            messages.error(request, "Already registered before")

        elif serializer.is_valid():
            serializer.save()
            logger.info(serializer.data)
            messages.success(request, "Project registration completed successfully")
            
        else:
            logger.error(serializer.errors)
            messages.error(request, "Project registration unsuccessful")
    
    else:
        if serializer.is_valid():
            serializer.save()
            logger.info(serializer.data)
            messages.success(request, "Project registration completed successfully")
        
        else:
            logger.error(serializer.errors)
            messages.error(request, "Project registration unsuccessful")

    return redirect('dashboard')

@api_view(['GET', 'POST'])
def submit_project(request):
    if request.method == 'POST':
        is_registered = ProjectRegistration.objects.filter(clg_id = request.data.get('clg_id'), is_submitted = 0).exists()

        if is_registered:
            parser_class = (FileUploadParser, )
            serializer = ProjectSubmissionSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                ProjectRegistration.objects.filter(clg_id = request.data.get('clg_id'), is_submitted = 0).update(is_submitted = 1)
                logger.info(serializer.data)
                messages.success(request, "Project submitted successfully")
            else:
                logger.error(serializer.errors)
                messages.error(request, "Project submition failed")
        else:
            logger.info("Student not registered any project under any faculty.")
            messages.warning(request, "Student not registered any project under any faculty.")
        
    return redirect('dashboard')


@api_view(['GET'])
def download_project(request):
    project = ProjectSubmission.objects.filter(project_id = request.query_params['id']).first()
    file_path = MEDIA_ROOT + str(project.project_file)
    # print('\n\n -->', file_path)
    # print('\n\n-->',MEDIA_ROOT)
    # print('\n\n-->', str(project.project_file))
    response = FileResponse(open(file_path,'rb'))
    logger.info(response)

    return response

# @api_view(['GET'])
# def view_notifications(request):
#     token = request.COOKIES.get('token', None)

#     if token==None:
#         logger.error("Token not exist")
#         return redirect("login-page")

#     try:
#         payload = jwt.decode(token, key, algorithms=['HS256'])
#         print(payload)
#     except jwt.ExpiredSignatureError:
#         return redirect("login-page")

#     user = User.objects.filter(email=payload['email']).first()

#     notifications = Notifications.objects.filter(clg_id = user.clg_id).all()

#     notifications = list(notifications.values())

#     print('----> ', notifications)

#     if notifications is not None:
#         Notifications.objects.filter(clg_id = user.clg_id, is_viewed = 0).update(is_viewed = 1)
        # return HttpResponse({'notifications':notifications})

    #return statement

# Faculty Apis

@api_view(['POST','GET'])
def create_notifications(request):
    token = request.COOKIES.get('token', None)

    if token==None:
        logger.error("Token not exist")
        return redirect("login-page")

    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
        print(payload)
    except jwt.ExpiredSignatureError:
        return redirect("login-page")

    if request.method == 'POST':
        user = User.objects.filter(email=payload['email']).first()

        faculty_name = user.first_name + " " + user.last_name
        if 'clg_id' in list(request.data.keys()):
            students_list=[{'clg_id':request.data['clg_id']}]
        else:
            students_list = list(ProjectRegistration.objects.filter(faculty = faculty_name, is_submitted = 0).all().values('clg_id'))

        new_dict={}
        new_dict.update(request.data)
        for k in new_dict.keys():
            new_dict[k]=new_dict[k][0]

        for i in students_list:
            new_dict['clg_id']= i['clg_id']
            new_dict['faculty'] = faculty_name
            serializer = NotificationsSerializer(data = new_dict)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                logger.info(serializer.data)
            else:
                logger.error(serializer.errors)
                print("Serializer Erros : ",serializer.errors)
    
        if serializer.is_valid():
            messages.info(request, 'Work assigned successfully')
        else:
            messages.error(request, 'Work assignment failed')

        return redirect('dashboard')
    return render(request,'project1/faculty-dashboard.html')

@api_view(['POST'])
def assign_marks(request):
    token = request.COOKIES.get('token', None)

    if token==None:
        logger.error("Token not exist")
        return redirect("login-page")

    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
        print(payload)
    except jwt.ExpiredSignatureError:
        return redirect("login-page")

    if request.method == "POST":
        already_exists = Marks.objects.filter(project_id = request.data['project_id']).exists()

        if already_exists:
            logger.info('Project marks already assigned')
            messages.error(request,'Marks already assigned for this project.')
        else:

            user = User.objects.filter(email=payload['email']).first()

            faculty_name = user.first_name + " " + user.last_name
            data = request.data.dict()
            data.update({'faculty':faculty_name})

            serializer = MarksSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                ProjectSubmission.objects.filter(project_id = request.data['project_id']).update(is_marked = 1)
                logger.info(serializer.data)
                messages.success(request, 'Marks assigned successfully')
            else:
                logger.error(serializer.errors)
                messages.error(request, "Marks assignment failed. Try again...")
            
            
        return redirect('scoreboard')
