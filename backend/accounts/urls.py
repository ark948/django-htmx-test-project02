from django.urls import path


from . import views


app_name = 'accounts'
urlpatterns = [
    path('redirect-to-home/', views.redirect_to_home, name='re-home'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
    path('email-login/', views.email_login, name='e-login'),
    path('', views.index, name='index'),
]