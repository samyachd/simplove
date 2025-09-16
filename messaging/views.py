from django.contrib.auth.decorators import login_required
from profiles.decorators import profile_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Thread
from .forms import MessageForm
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()


@profile_required
@login_required
def new_thread(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if target == request.user:
        messages.error(request, "Tu ne peux pas t'envoyer un message à toi-même.")
        return redirect("matches:my_matches")

    # Vérifie si un thread existe déjà entre les deux
    thread = (
        Thread.objects.filter(participants=request.user)
        .filter(participants=target)
        .first()
    )
    if not thread:
        thread = Thread.objects.create()
        thread.participants.add(request.user, target)

    return redirect("messaging:thread_detail", pk=thread.pk)


@profile_required
@login_required
def thread_list(request):
    threads = request.user.threads.all()
    return render(request, "thread_list.html", {"threads": threads})


@profile_required
@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk, participants=request.user)
    messages = thread.messages.order_by("timestamp")

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.thread = thread
            msg.save()
            return redirect("messaging:thread_detail", pk=pk)
    else:
        form = MessageForm()

    return render(
        request,
        "thread_detail.html",
        {"thread": thread, "messages": messages, "form": form},
    )
