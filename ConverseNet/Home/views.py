from datetime import datetime

import openai as openai
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
# Create your views here.
import json
from .models import ConverseNetUser, Profile, Bot_Message, FriendsThread, Requests, FriendsThreadMessage, Diary


# def getMessages(request, thread_id):
#     friends = FriendsThread.objects.get(id=thread_id)  # thread model
#     message_collection = FriendsThreadMessage.objects.filter(thread_Id=friends.id)  # message model
#     messages = []
#     for message in message_collection:
#         chat = message.message
#         time = message.friends_Chat_Time.strftime("%m/%d/%Y, %H:%M:%S")
#         sender = ConverseNetUser.objects.get(id=message.sender_Id.id)
#         sender_name = sender.first_name + " " + sender.last_name
#         is_user_message = sender.id == request.user.id  # Check if the sender is the current user
#         messages.append({
#             "text": chat,
#             "sender_name": sender_name,
#             "is_user_message": is_user_message,
#             "time": time,
#         })
#     return messages


def botchat(request, user_name):
    user = User.objects.get(username=user_name)
    username = user.first_name + ' ' + user.last_name
    client = ConverseNetUser.objects.get(user_ID=user.id)
    client_id = client.id
    lists = getMessagesRobo(request, user_id=client_id)
    prompt_list: list[str] = ['You are a Chatbot and will answer as a Chatbot',
                              '\nHuman: What time is it?',
                              '\nAI: I have no idea, I\'m a Chatbot!']
    if request.method == 'POST':
        message = request.POST['message']
        if message != '':
            response: str = get_bot_response(message, prompt_list)
            new_msg = Bot_Message(converseNet_user_Message=message, reply_Message=response,
                                  converseNet_user=client)
            new_msg.save()
            # get the previous messages from record
            lists = getMessagesRobo(request, user_id=client_id)
            return HttpResponseRedirect(reverse('botchat', kwargs={'user_name': user_name}))
        else:
            pass  # url name= diary and url er argument lagbe tai kwargs use kora lagse
    return render(request, 'Home/botchat.html', {'user_full_name': username.upper(),
                                                 'user_name': user_name,
                                                 'messages': lists})


def getMessages(request, thread_id):
    # Original list
    messages = FriendsThreadMessage.objects.filter(thread_Id=thread_id)
    list1=list(messages.values())
    # Create a new list with sender_name
    new_list = []
    for item in list1:
        sender_id = item['sender_Id_id']
        sender = ConverseNetUser.objects.get(id=sender_id)
        sender_name = sender.first_name + " " + sender.last_name
        item['sender_name'] = sender_name
        item.pop('sender_Id_id')  # Remove the old key
        new_list.append(item)
    # Print the new list
    # print(new_list)
    # for key in list1:
    #     print(list1[key])
    # messages=FriendsThreadMessage.objects.filter(thread_Id=thread_id)
    # print("here'''''''''''''')")
    print(list(messages.values()))
    return JsonResponse({"messages": new_list})


def inbox_page(request, friend_name, thread_id, user_name):
    list_of_messages = getMessages(request, thread_id=thread_id)
    user = User.objects.get(username=user_name)
    userid = user.id
    if request.method == 'POST':
        message = request.POST['message']
        # room_details = Room.objects.get(name=room)
        # messages = Message.objects.filter(room=room_details.id)
        # return JsonResponse({"messages": list(messages.values())})
        if message != '':
            fuser = ConverseNetUser.objects.get(user_ID=userid)
            friends_thread = FriendsThread.objects.get(id=thread_id)
            new_message = FriendsThreadMessage(message=message, sender_Id=fuser, thread_Id=friends_thread)
            new_message.save()
            list_of_messages = getMessages(request, thread_id=thread_id)
            return HttpResponseRedirect(reverse('inbox', kwargs={
                'friend_name': friend_name,
                'thread_id': thread_id,
                'user_name': user_name}))
    return render(request, 'Home/chat.html', {'friend_name': friend_name,
                                              'user_name': user_name,
                                              'thread_id': thread_id,
                                              'messages': list_of_messages,
                                              'userid': userid})


# def inbox_page(request, friend_name, thread_id, user_name):
#     list_of_messages = getMessages(request, thread_id=thread_id)
#     user = User.objects.get(username=user_name)
#     userid = user.id
#     if request.method == 'POST':
#         message = request.POST['message']
#         # room_details = Room.objects.get(name=room)
#         # messages = Message.objects.filter(room=room_details.id)
#         # return JsonResponse({"messages": list(messages.values())})
#         messages = FriendsThreadMessage.objects.filter(thread_ID=thread_id)
#         return JsonResponse({"messages": list(messages.values())})
#         if message != '':
#             fuser = ConverseNetUser.objects.get(user_ID=userid)
#             friends_thread = FriendsThread.objects.get(id=thread_id)
#             new_message = FriendsThreadMessage(message=message, sender_Id=fuser, thread_Id=friends_thread)
#             new_message.save()
#             list_of_messages = getMessages(request, thread_id=thread_id)
#             return HttpResponseRedirect(reverse('inbox', kwargs={
#                 'friend_name': friend_name,
#                 'thread_id': thread_id,
#                 'user_name': user_name}))
#     return render(request, 'Home/chat.html', {'friend_name': friend_name,
#                                               'user_name': user_name,
#                                               'thread_id': thread_id,
#                                               'messages': list_of_messages,
#                                               'userid': userid})

def addfriend_page(request, user_name):
    if User.objects.filter(username=user_name).exists():
        user = User.objects.get(username=user_name)
        user_email = user.email
        if request.method == 'POST':
            friend_email = request.POST['friend_email']
            value = 'T'
            user = ConverseNetUser.objects.all()
            if user_email != friend_email:
                if user.filter(email=user_email).exists() and user.filter(email=friend_email).exists():
                    us1 = ConverseNetUser.objects.get(email=user_email)
                    us2 = ConverseNetUser.objects.get(email=friend_email)
                    fi1 = FriendsThread.objects.filter(friends_User_id_Person1=us1)
                    for fi in fi1:
                        if fi.friends_User_id_Person2 == us2:
                            value = 'f'
                            break
                    fi1 = FriendsThread.objects.filter(friends_User_id_Person2=us1)
                    for fi in fi1:
                        if fi.friends_User_id_Person1 == us2:
                            value = 'f'
                            break
                    if value == 'T':
                        u1 = FriendsThread(friends_User_id_Person1=us1, friends_User_id_Person2=us2)
                        u1.save()
                        return redirect('homepage', user_name=user_name)
                    else:
                        messages.error(request, 'ALREADY A FRIEND !! ')
                else:
                    messages.error(request, 'THE PERSON DO NOT EXIST!')
            else:
                messages.error(request, 'INVALID INPUT!')
        return render(request, 'Home/addfriend.html', {'user_name': user_name})





def login(request):
    if request.method == 'POST':
        client_email = request.POST['email1']
        client_password = request.POST['password1']
        if User.objects.filter(email=client_email).exists():
            users = User.objects.filter(email=client_email)
            for user in users:
                if user.password == client_password:
                    messages.success(request, 'Successfully Logged In.')
                    return redirect('homepage', user_name=user.username)
                else:
                    messages.error(request, 'Incorrect Password !! ')
        else:
            messages.error(request, 'Username does not exist. ')
    return render(request, 'Home/login.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        name = first_name + email
        if User.objects.filter(username=name).exists():
            messages.error(request, 'The person with this email is already a member...')
        elif password != confirm_password:
            messages.error(request, 'The passwords do not match...')
        else:
            user = User(password=password, username=name, last_name=last_name, email=email, first_name=first_name)
            user.save()
            user_again = User.objects.all()
            get_user = user_again.get(email=email)
            date_of_birth = request.POST['date_of_birth']
            gender = request.POST['gender']
            client = ConverseNetUser(first_name=first_name, last_name=last_name, email=email, gender=gender,
                                     password=password, Date_Of_Birth=date_of_birth, user_ID=get_user)
            client.save()
            return render(request, 'Home/login.html')

    return render(request, 'Home/signup.html')


def getMessagesRobo(request, user_id):
    messages = []
    if Bot_Message.objects.filter(converseNet_user=user_id).exists():
        msgs = Bot_Message.objects.filter(converseNet_user=user_id)
        for message in msgs:
            user_chat = message.converseNet_user_Message
            reply = message.reply_Message
            time = message.message_Time.strftime("%m/%d/%Y, %H:%M:%S")

            user_message = {
                'text': user_chat,
                'sender': 'user',
                'time': time,
            }
            bot_message = {
                'text': reply,
                'sender': 'bot',
                'time': time,
            }
            messages.append(user_message)
            messages.append(bot_message)
    return messages


def getPreviousNotes(request, user_id):
    lists = []
    if Diary.objects.filter(converseNet_user=user_id).exists():
        client_notes = Diary.objects.filter(converseNet_user=user_id)
        # notes_id = notes.id
        # notes = Diary.objects.filter(Thread_Id=thread_Id)
        for notes in client_notes:
            title = str('Title : ' + notes.title)
            time = str('Time : ' + notes.time.strftime("%m/%d/%Y, %H:%M:%S"))
            note = str('Notes: ' + notes.note + '\n')
            str1 = '\n'.join([title, time, note])
            lists.append(str1)
    return lists


def diary(request, user_name):
    user = User.objects.get(username=user_name)
    client = ConverseNetUser.objects.get(user_ID=user.id)
    client_id = client.id
    lists = getPreviousNotes(request, user_id=client_id)
    lists.reverse()
    if request.method == 'POST':
        notes = request.POST['notes']
        title = request.POST.get('title')

        if notes != '' and title != '':
            note = Diary(converseNet_user=client, title=title, note=notes)
            note.save()
            return HttpResponseRedirect(reverse('diary', kwargs={
                'user_name': user_name}))  # url name= diary and url er argument lagbe tai kwargs use kora lagse
        else:
            messages.error(request, 'PLEASE FILL UP TITLE AND NOTES FIELD')
    name = str(client.first_name + " " + client.last_name).upper()
    return render(request, 'Home/diary.html', {'user_name': user_name,
                                               'name': name,
                                               'notes': lists,
                                               })


def loadpage(request):
    return render(request, 'Home/loadpage.html', {})


def homepage(request, user_name):
    if request.method == 'POST':
        friend_email = request.POST['email']
        cuser = User.objects.get(username=user_name)
        user = ConverseNetUser.objects.get(user_ID=cuser.id)

        if User.objects.filter(email=friend_email).exists():  # if that user exists
            cfriend_user = User.objects.get(email=friend_email)
            friend_user = ConverseNetUser.objects.get(user_ID=cfriend_user.id)
            flag = 0
            if user is not None and friend_user is not None:
                friendship_thread_of_user_where_user_is_person_1 = FriendsThread.objects.filter(
                    friends_User_id_Person1=user)
                for thread in friendship_thread_of_user_where_user_is_person_1:
                    if thread.friends_User_id_Person2 == friend_user:
                        flag = 1
                        thread_id = thread.id
                        break
                friendship_thread_of_user_where_user_is_person_2 = FriendsThread.objects.filter(
                    friends_User_id_Person2=user)
                for thread in friendship_thread_of_user_where_user_is_person_2:
                    if thread.friends_User_id_Person1 == friend_user:
                        thread_id = thread.id
                        flag = 1
                        break
                if flag == 1:
                    return redirect('inbox', friend_name=cfriend_user.first_name + ' ' + friend_user.last_name,
                                    thread_id=thread_id, user_name=cuser.username)
                else:
                    messages.error(request, 'you are not friends with this person !! ')
        else:
            messages.error(request, 'NO SUCH PERSON EXISTS !!')
    return render(request, 'Home/homepage.html', {'user_name': user_name, })


def profile(request, user_name):
    user = User.objects.get(username=user_name)
    client = ConverseNetUser.objects.get(user_ID=user.id)
    if request.method == 'POST':
        about_info = request.POST['about_info']
        if about_info != '':
            # to check if the profile already exists
            if Profile.objects.filter(converseNet_user=client.id).exists():
                p = Profile.objects.get(converseNet_user=client.id)
                p.bio = about_info
                p.save()
            else:
                pro = Profile(bio=about_info, converseNet_user=client)
                pro.save()
    name = str(client.first_name + " " + client.last_name).upper()
    birth_date = client.Date_Of_Birth
    email = client.email
    gender = str(client.gender).upper()
    profile = Profile.objects.filter(converseNet_user=client.id)
    if profile.exists():
        p = Profile.objects.get(converseNet_user=client.id)
        about = p.bio
    else:
        about = "USER HAS NOT ADDED ANY BIO OR PIC YET!!!!"  # hi i am oishi
    return render(request, 'Home/profile.html', {'user_name': user_name,
                                                 'name': name,
                                                 'bod': birth_date, 'bio': about,
                                                 'email': email,
                                                 'gender': gender})


# previous bot
with open('Home/hidden.txt') as file:
    openai.api_key = file.read()


def get_api_response(prompt: str) -> str | None:
    text: str | None = None
    try:
        response: dict = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=60,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0,
            stop=["You:"]
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print('ERROR:', e)

    return text


def update_list(message: str, pl: list[str]):
    pl.append(message)


def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt


def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    print(prompt)
    bot_response: str = get_api_response(prompt)
    print(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something went wrong...'

    return bot_response


def password_reset(request, user_name):
    user = User.objects.get(username=user_name)
    username = user.first_name + ' ' + user.last_name
    if (request.method == 'POST'):
        password = request.POST['password']
        if user.password == password:
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            if new_password != '' and confirm_password != '':
                if new_password == confirm_password:
                    user.password = new_password
                    user.save()
                    client = ConverseNetUser.objects.get(user_ID=user.id)
                    client.password = new_password
                    client.save()
                    messages.success(request, 'Password updated.')
                    return redirect('profile', user_name=user_name)
                else:
                    messages.error(request, 'THE PASSWORDS DOES NOT MATCH !!!...')
            else:
                messages.error(request, 'Empty string not allowed as password!!!!')
        else:
            messages.error(request, 'WRONG USER PASSWORD ENTERED!!!!')

    return render(request, 'Home/updatepassword.html', {'user_name': username})



def addfriend_page(request, user_name):
    if User.objects.filter(username=user_name).exists():
        user = User.objects.get(username=user_name)
        user_email = user.email
        if request.method == 'POST':
            friend_email = request.POST['friend_email']
            value = 'T'
            user = ConverseNetUser.objects.all()
            if user_email != friend_email:
                if user.filter(email=user_email).exists() and user.filter(email=friend_email).exists():
                    us1 = ConverseNetUser.objects.get(email=user_email)
                    us2 = ConverseNetUser.objects.get(email=friend_email)
                    fi1 = FriendsThread.objects.filter(friends_User_id_Person1=us1)
                    for fi in fi1:
                        if fi.friends_User_id_Person2 == us2:
                            value = 'f'
                            break
                    fi1 = FriendsThread.objects.filter(friends_User_id_Person2=us1)
                    for fi in fi1:
                        if fi.friends_User_id_Person1 == us2:
                            value = 'f'
                            break
                    if value == 'T':
                        u1 = FriendsThread(friends_User_id_Person1=us1, friends_User_id_Person2=us2)
                        u1.save()
                        # Get the list of friends for the user
                        friends_list = FriendsThread.objects.filter(friends_User_id_Person1=us1)
                        return render(request, 'Home/addfriend.html', {'user_name': user_name, 'friends_list': friends_list})
                    else:
                        messages.error(request, 'ALREADY A FRIEND !! ')
                else:
                    messages.error(request, 'THE PERSON DO NOT EXIST!')
            else:
                messages.error(request, 'INVALID INPUT!')
        else:
            # Get the list of friends for the user
            us1 = ConverseNetUser.objects.get(email=user_email)
            friends_list = FriendsThread.objects.filter(friends_User_id_Person1=us1)
            return render(request, 'Home/addfriend.html', {'user_name': user_name, 'friends_list': friends_list})

