from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Block

from .models import Chat, Message

User = get_user_model()


@login_required
def messages_home(request):
    users = User.objects.exclude(id=request.user.id)
    return render(
        request,
        "user_list.html",
        {"users": users}
    )


@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    chat = (
        Chat.objects.filter(participants=request.user)
        .filter(participants=other_user)
        .first()
    )

    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)

    if request.method == "POST":
        content = request.POST.get("message")
        if content:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                content=content
            )
        return redirect("chat", user_id=other_user.id)

    messages = chat.messages.order_by("timestamp")
    is_blocked = Block.objects.filter(
    blocker=request.user,
    blocked=other_user).exists()
    
    return render(
    request,
    "chat.html",
    {
        "other_user": other_user,
        "messages": messages,
        "is_blocked": is_blocked,
    }
)



from .models import Block
@login_required
def delete_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    chat = (
        Chat.objects.filter(participants=request.user)
        .filter(participants=other_user)
        .first()
    )
    if chat:
        chat.delete()
    return redirect("messages_home")

@login_required
def block_user(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    Block.objects.get_or_create(
        blocker=request.user,
        blocked=other_user
    )

    return redirect("chat", user_id=other_user.id)



@login_required
def unblock_user(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    Block.objects.filter(
        blocker=request.user,
        blocked=other_user
    ).delete()

    return redirect("chat", user_id=other_user.id)
