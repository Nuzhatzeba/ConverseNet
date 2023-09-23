import openai as openai
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
# Create your views here.

from .models import ConverseNetUser, Profile, Bot_Message, FriendsThread, Requests, FriendsThreadMessage, Diary


# from .forms import ClientForm


def login(request):
    if request.method == 'POST':
        client_email = request.POST['email1']
        client_password = request.POST['password1']
        print("here")
        if User.objects.filter(email=client_email).exists():
            users = User.objects.filter(email=client_email)
            for user in users:
                if user.password == client_password:
                    messages.success(request, 'Sucessfully Logged In.')
                    return redirect('homepage', user_name=user.username)
                else:
                    messages.error(request, 'Incorrect Password !! ')
        else:
            messages.error(request, 'Username does not exist. ')
    print("nope here")
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


def chat(request):
    return render(request, 'Home/chat.html')


def getMessagesRobo(request, user_id):
    lists = []
    if Bot_Message.objects.filter(converseNet_user=user_id).exists():
        msgs = Bot_Message.objects.filter(converseNet_user=user_id)
        lists = []
        for message in msgs:
            user_chat = message.converseNet_user_Message
            reply = message.reply_Message
            time = message.Message_Time.strftime("%m/%d/%Y, %H:%M:%S")
            history1 = str('YOU  :' + user_chat + ', TIME :' + time)
            lists.append(history1)
            history2 = str('BOT  :' + reply + '\n' + ', TIME :' + time)
            lists.append(history2)
    return lists


def inbox(request, user_name):
    pass


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
                                  converseNet_user=client_id)
            new_msg.save()
            # get the previous messages from record
            lists = getMessagesRobo(request, user_id=client_id)
        else:
            return HttpResponseRedirect(reverse('botchat', kwargs={
                'user_name': user_name}))  # url name= diary and url er argument lagbe tai kwargs use kora lagse
    return render(request, 'Home/botchat.html', {'user_full_name': username.upper(),
                                                 'user_name': user_name,
                                                 'messages': lists})


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
