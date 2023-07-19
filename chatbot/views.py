from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth.models import User
from . models import Chat
from django.utils import timezone
# Create your views here.
openai_api_key = '####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'
openai.api_key = openai_api_key
def ask_openai(message):
    # response = openai.Completion.create(
    #     model = 'text-davinci-003',
    #     prompt = message,
    #     max_tokens=200,
    #     n = 1,
    #     stop= None,
    #     temperature=0.7,
    # )
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo-16k',
        messages = [
            {"role":"system","content":"You are a helpful assistant"},
            {'role':"user","content":message}
        ]
    )
    answer = response.choices[0].message.content.strip()
    return answer


def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response':response})
    return render(request, 'chatbot.html',{'chats':chats})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invallid Username or Password'
            return render(request, 'login.html', {'error_message':error_message})
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request,user)
                return redirect('chatbot')
            except:
                error_message = "Error while Creating Account"
                return render(request, 'register.html',{"error_message":error_message})
        else:
            error_message = "Password does not matched"
            return render(request, 'register.html', {'error_message':error_message})
    return render(request, 'register.html')