from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name='overview'),
    path('register/', views.register_user, name='register'),   
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('messages/', views.general_message_actions, name='messages'), 
    path('sent/', views.user_sent_messages, name='sent'), 
    path('messages/<int:id>', views.specific_message_actions, name='specific message'), 
    path('unread/', views.unread_message_actions, name='unread'), 

]