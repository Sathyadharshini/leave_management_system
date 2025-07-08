from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('apply/', views.apply_leave, name='apply_leave'),
    path('my-leaves/', views.my_leaves, name='my_leaves'),
    path('manage/', views.manage_leaves, name='manage_leaves'),
    path('approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
    path('test-email/', views.test_email, name='test_email'),


]
