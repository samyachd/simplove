from django.contrib.auth.decorators import login_required
from profiles.decorators import profile_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Thread
from .forms import MessageForm

@profile_required
@login_required
def thread_list(request):
    threads = request.user.thread.all()
    return render(request, "thread_list.html", {"threads": threads})

@profile_required
@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk, participants=request.user)
    messages = thread.message.order_by('timestamp')

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.thread = thread
            msg.save()
            return redirect('messaging:thread_detail', pk=pk)
    else:
        form = MessageForm()

    return render(request, "thread_detail.html", {
        "thread": thread,
        "messages": messages,
        "form": form
    })