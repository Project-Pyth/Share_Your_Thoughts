from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.static import serve

urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('blog/',views.blog,name='blog'),
    path('logout',views.logout,name='logout'),
    path('profile',views.profile,name='profile'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('change_password',views.change_password,name="change_password"),
    path('view_blog',views.view_blog,name="view_blog"),
    path('reset_password',auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('blogpost/<int:id>',views.blogpost,name='blogpost'),
    path('blogpost/postcomment',views.postcomment,name='postcomment'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    path('allblog',views.allblog,name='allblog'),
    path('search_blogs',views.search_blogs,name='search_blogs'),
    path('about_us',views.about_us,name='about_us'),

]

