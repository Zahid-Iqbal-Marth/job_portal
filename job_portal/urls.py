"""job_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include # new
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from user import views as user_views

from job import views as job_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', job_views.home,name='job-home'),
    path('register/',user_views.register,name="user-register"),
    path('profile/',user_views.manageProfile,name="user-profile"),
    path('login/',auth_views.LoginView.as_view(template_name='user/login.html'),name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='user/logout.html'),name="logout"),
    
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'),name="password_reset"),
    
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),name="password_reset_done"),

    path('password-reset-confirm/<uid64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),name="password_reset_confirm"),




    path('resume/add/',user_views.AddResume,name="user-addresume"),
    path('resume/my/',user_views.MyResume,name="user-myresume"),
    path('resume/view/<int:pk>',user_views.viewResume,name="user-viewresume"),
    path('resume/update/<int:pk>',user_views.updateResume,name="user-updateresume"),
    path('resume/delete/<int:r_pk>',user_views.deleteResume,name="user-deleteresume"),
    #new added
    path('resume/select/<int:j_pk>', user_views.SelectResume, name='user-selectresume'),
    path('resume/select/<int:j_pk>/<int:r_id>', user_views.userApplied, name='user-applied'),





    path('post/new/', job_views.PostCreateView, name='post-create'),
    path('', job_views.home, name='job-home'),
    path('post/<int:pk>/', job_views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', job_views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', job_views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<str:SearchWord>/search', job_views.Search, name='post-search'),


    path('post/my/', job_views.MyJobs, name='user-myjob'),

    
    #new added

    path('post/<int:pk>/application', job_views.applicants, name='post-applicants'),
    path('post/<int:j_pk>/application/<int:r_pk>',job_views.detailApplicants,name="post-detailapplicants"),

    # pricing urls
    path('pricing',job_views.ViewPricingTable,name='pricing'),
    path('charge/<int:pk>', job_views.Charge, name='charge'), # new
    path('checkout/<int:pk>', job_views.viewCheckoutPage, name='checkout'),
    

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)