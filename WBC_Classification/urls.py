"""
URL configuration for WBC_Classification project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from WBC_Classification import views as mainView
from Admin import views as av
from users import views as usr
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from users import views as uv



urlpatterns = [
    path('admin/', admin.site.urls),
    path("", mainView.index, name="index"),
    path("index", mainView.index, name="index"),
    path("Adminlogin", mainView.AdminLogin, name="AdminLogin"),
    path("UserLogin", mainView.UserLogin, name="UserLogin"),
    path('AdminHome', mainView.adminhome, name='AdminHome'),
  
    # admin views
    path("AdminLogincheck", av.AdminLoginCheck, name="AdminLoginCheck"),
    path('userDetails', av.RegisterUsersView, name='RegisterUsersView'),
    path('ActivUsers/', av.ActivaUsers, name='activate_users'),
    path('DeleteUsers/', av.DeleteUsers, name='delete_users'),
    path('viewUserDetails/', av.viewUserDetails, name='viewUserDetails'),
    path('adminNotifications/', av.adminNotifications, name='adminNotifications'),
    path('markAdminNotificationRead/', av.markAdminNotificationRead, name='markAdminNotificationRead'),
    path('passwordResetRequests/', av.passwordResetRequests, name='passwordResetRequests'),
    path('approvePasswordReset/', av.approvePasswordReset, name='approvePasswordReset'),
    path('rejectPasswordReset/', av.rejectPasswordReset, name='rejectPasswordReset'),
    path('helpTickets/', av.helpTickets, name='helpTickets'),
    path('markHelpTicketSolved/', av.markHelpTicketSolved, name='markHelpTicketSolved'),
    path('markHelpTicketInProgress/', av.markHelpTicketInProgress, name='markHelpTicketInProgress'),

    #userurls
    path('UserRegisterForm',uv.UserRegisterActions,name='UserRegisterForm'),
    path("UserLoginCheck/", usr.UserLoginCheck, name="UserLoginCheck"),
    path("UserHome/", usr.UserHome, name="UserHome"),
    path("predictions/", usr.predictions, name="predictions"),
    path("training/", usr.training, name="training"),
    path("accuracy/", usr.accuracy, name="accuracy"),
    path("index/", usr.index, name="index"),
    path("view_results/", usr.view_results, name="view_results"),
    path("clear_history/", usr.clear_history, name="clear_history"),
    path("training_history/", usr.training_history, name="training_history"),
   

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

