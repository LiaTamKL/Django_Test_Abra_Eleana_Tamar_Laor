from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .DAL.AccountDAL import AccountDAL
from rest_framework.permissions import IsAuthenticated


# Create your views here.

@api_view(['GET'])
def api_overview(request):
    api_urls ={
        'Register (POST)':'/register/',
        'Logout (GET)':'/logout/',
        'Login (POST)':'/login/',
        'All Messages (GET), Write message (POST)':'/messages/',
        'Get Specific Message (GET), Delete message (DELETE)':'/messages/<int:pk>',
        'Get Unread (GET)':'/unread/',
    }
    return Response(api_urls)

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        """Requires email and password field that match a pair in the database.
        Will not work if a user is already logged in"""
        result = AccountDAL.login(request)
        return result

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Will not work if a user is not logged in"""
    if request.method == 'GET':
        result = AccountDAL.logout(request)
        return result

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        """Requires password, password2, email and username. First two must match, second two must be unique"""
        print(request.data)
        result = AccountDAL.register_account(request.data)
        return result


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def general_message_actions(request):

    if request.method == 'GET':
        result = AccountDAL.get_all_account_messages(request.user)
        return result

    if request.method == 'POST':
        """Needs by_user=[username] and content=[text]."""
        result = AccountDAL.write_message(details=request.data, sender=request.user.username)
        return result

@api_view(['DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def specific_message_actions(request, id):

    if request.method == 'GET':
        result = AccountDAL.get_specific_message(id=id, account=request.user)
        return result

    if request.method == 'DELETE':
        result = AccountDAL.delete_message(id=id, account=request.user)
        return result

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_message_actions(request):

    if request.method == 'GET':
        result = AccountDAL.get_unread_messages(request.user)
        return result
