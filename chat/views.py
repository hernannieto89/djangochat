# chat/views.py
from django.contrib.auth import login,  authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from chat.models import ChatMessage
from django.views import generic


class IndexView(generic.View):

    def get(self, request):
        chat_queryset = ChatMessage.objects.order_by("-created")[:50]
        chat_message_count = len(chat_queryset)
        if chat_message_count > 0:
            first_message_id = chat_queryset[len(chat_queryset) - 1].id
        else:
            first_message_id = -1
        previous_id = -1
        if first_message_id != -1:
            try:
                previous_id = ChatMessage.objects.filter(pk__lt=first_message_id).order_by("-pk")[:1][0].id
            except IndexError:
                previous_id = -1
        chat_messages = reversed(chat_queryset)

        messages_raw = ''
        for message in chat_messages:
            messages_raw += message.message + '\n'

        return render(request, "chat/room.html", {
            'chat_messages': messages_raw,
            'first_message_id': previous_id
        })


def register_view(request):
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

