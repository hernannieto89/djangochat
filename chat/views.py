# chat/views.py
from django.contrib.auth import login,  authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from chat.utils import get_last_messages
from chat.forms import ProfileForm


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def update_profile(request):
    """
    Updates User profile.
    :param request: Request Object
    :return: HttpResponse
    """
    msg = ''
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            msg = 'Your profile was successfully updated!'
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/profile.html', {
        'user_name': request.user,
        'profile_form': profile_form,
        'messages': msg
    })
