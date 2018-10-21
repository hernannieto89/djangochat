# chat/views.py
from django.contrib.auth import login,  authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from chat.utils import  get_last_messages


def index_view(request):
    """
    Index view for chat room.
    :param request: Request Object
    :return: HttpResponse
    """

    return render(request, "chat/room.html", {
        'chat_messages': get_last_messages()
    })


def register_view(request):
    """
    Register view for chat room.
    :param request: Request Object
    :return: HttpResponse
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
