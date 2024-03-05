# from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import  profile, login_user, register_user, forgot_password, logout_user, get_user, reset_password #, change_password , verify_user
from .site_apis import display_dashboard, display_about, display_scoreboard, register_project, submit_project, download_project, create_notifications, assign_marks #, FileUploadView 

urlpatterns = [
    path('register/', register_user, name="register-page"),
    path('login/', login_user, name="login-page"),
    path('myProfile/', get_user, name="profile-page"),
    path('logout/', logout_user, name="logout"),
    # path('verify_user/', verify_user),
    # path('change_password', change_password),
    path('forgot_password/', forgot_password, name="forgot-pswd"),
    path('reset_password', reset_password, name="reset-pswd"),
    path('editProfile/', profile, name="edit-profile"),
    path('user-dashboard/', display_dashboard, name="dashboard"),
    path('scoreboard/', display_scoreboard, name="scoreboard"),
    path('about-Devs/', display_about, name="about-page"),

    path('register_project', register_project, name="register_project"),
    path('submit_project', submit_project, name="submit_project"),
    path('download_project', download_project, name="download_project"),
    path('create_notifications', create_notifications, name = "create_notifications"),
    # path('view_notifications', view_notifications, name='view_notifications'),
    path('assign_marks', assign_marks, name="assign_marks")
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)