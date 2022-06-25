from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout

class AccountDAL():

    def __check_if_exist_check_if_of_account(id,account):
        """Takes id and account. 
        if message does not exist, returns 404.
        if message is not to the account, returns 400.
        if good, sends the message.
        """
        try:
            message = Message.objects.get(pk=id)
        except:
            return 404
        if message.to_user != account and message.by_user != account:
            return 400
        
        return message


    def register_account(application):
        """Takes application. 
        Returns 200 if valid, returns 400 and errors if bad request.
        """
        try:
            if application['password'] !=application['password2']:
                return Response(data='Passwords must match',status=status.HTTP_400_BAD_REQUEST)
        except: return Response(data='Password and password2 required',status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AccountSerializer(data=application)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return Response(data=f'User:{user.username} created successfully.')
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def login(request):
        """
        Takes login details and request. Logs user in if password and email match a user.
        Returns a 400 status otherwise (if they don't match or if either was not entered).
        """
        if request.user.is_authenticated:
            return Response(f'Please logout first {request.user.username}!.', status=status.HTTP_400_BAD_REQUEST)

        try:
            email = request.data["email"]
            password = request.data["password"]
        except:
            return Response('Missing either email or password!.', status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return Response('Logged in successfully')
        return Response('Email and password do not match.', status=status.HTTP_400_BAD_REQUEST)

    def logout(request):
        """Logs out a user. If they're not logged in, sends status 400"""
        if request.user.is_authenticated:
            logout(request)
            return Response('Logged out')
        else: return Response('Not logged in!.', status=status.HTTP_400_BAD_REQUEST)

    def get_all_account_messages(account):
        """Takes account. 
        Returns all messages for said account.
        """
        context = {}
        messages = Message.objects.filter(to_user=account)
        sent_messages = Message.objects.filter(by_user=account)
        serializer = MessageSerializer(messages, many=True)
        second_serializer = MessageSerializer(sent_messages, many=True)
        context['received'] = serializer.data
        context['sent'] = second_serializer.data
        return Response(data=context)


    def get_unread_messages(account):
        """takes account. 
        returns all unread messages for said account.
        """
        unread_list =[]
        unread = Unread.objects.all()
        for mes in unread:
            unread_list.append(mes.message.id)
        print(unread_list)
        messages = Message.objects.filter(to_user=account).filter(id__in=unread_list)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def get_sent_messages(account):
        """takes account. 
        returns all messaged sent by said account.
        """
        messages = Message.objects.filter(by_user=account)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


    def delete_message(id, account):
        """Takes id and account. 
        if message does not exist, returns status 404.
        if message is not to/by the account, returns status 400.
        if good, deletes message, sends status 200.
        """
        message = AccountDAL.__check_if_exist_check_if_of_account(id, account)
        if message == 404:
            return Response(data='Message does not exist.', status=status.HTTP_404_NOT_FOUND)
        if message == 400:
            return Response(data='Message does not belong to logged in user.', status=status.HTTP_400_BAD_REQUEST)
        
        message.delete()
        try: 
            unread_status = Unread.objects.get(message=message)
            unread_status.delete()
        except:
            pass
        return Response(data=f'Message #{id}, successfully deleted by {account}')
    
    def get_specific_message(id, account):
        """Takes id and account. 
        if message does not exist, returns status 404.
        if message is not to/by the account, returns status 400.
        turns read status to true if the logged in user is the to_user.
        if good, returns message, sends status 200.
        """
        message = AccountDAL.__check_if_exist_check_if_of_account(id, account)
        if message == 404:
            return Response(data='Message does not exist.', status=status.HTTP_404_NOT_FOUND)
        if message == 400:
            return Response(data='Message does not belong to logged in user.', status=status.HTTP_400_BAD_REQUEST)
        
        if message.to_user == account:
            message.read = True
            message.save()
            try:
                unread_status = Unread.objects.get(message=message)
                unread_status.delete()
            except:
                pass
        serializer = MessageSerializer(message, many=False)
        return Response(data=serializer.data)

    def write_message(details, sender):
        """takes request data and sender's username. 
        If sender=receiver, sends status 400. If receiver doesn't exist, sends status 404.
        If details are missing in JSON, returns status 400 with errors.
        Otherwise, creates new message.
        """
        details['by_user'] = sender
        by = Account.objects.get(username=sender)


        if details['to_user'] == sender:
            return Response(data='You cannot send a message to yourself!', status=status.HTTP_400_BAD_REQUEST)

        try:
            to = Account.objects.get(username=details['to_user'])
        except Account.DoesNotExist:
            return Response(data='Receiver does not exist!', status=status.HTTP_404_NOT_FOUND)
        
        serializer = MessageSerializer(data=details, many=False)
        if serializer.is_valid():
            new_message = Message()
            new_message.by_user = by
            new_message.to_user = to
            new_message.content = details['content']
            new_message.subject = details['subject']
            new_message.save()
            unread_status = Unread()
            unread_status.message = new_message
            unread_status.save()
            return Response('Message created')
        else:
           return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)