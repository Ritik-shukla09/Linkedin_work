from django.shortcuts import render

# Create your views here.
# connections/views.py


import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import ConnectionRequest, Follow

User = get_user_model()
# my network page



from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import ConnectionRequest

User = get_user_model()
from .models import ConnectionRequest, Follow
from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import never_cache

@never_cache
@login_required
def my_network(request):
    users = User.objects.exclude(id=request.user.id)
    data = []
    print("NETWORK USERS:", list(users))
    for user in users:
        is_connected = ConnectionRequest.objects.filter(
            sender=request.user,
            receiver=user,
            status="accepted"
        ).exists() or ConnectionRequest.objects.filter(
            sender=user,
            receiver=request.user,
            status="accepted"
        ).exists()

        is_following = Follow.objects.filter(
            follower=request.user,
            following=user
        ).exists()

        data.append({
            "user": user,
            "is_connected": is_connected,
            "is_following": is_following,
        })

    return render(request, "Connections/my_network.html", {"data": data})


@login_required
def send_connection_request(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    data = json.loads(request.body)
    user_id = data.get("user_id")

    if int(user_id) == request.user.id:
        return JsonResponse({"error": "Cannot connect to yourself"}, status=400)

    receiver = User.objects.get(id=user_id)

    existing = ConnectionRequest.objects.filter(
        sender=request.user,
        receiver=receiver
    ).first()

    # Already connected
    if existing and existing.status == "accepted":
        return JsonResponse({"status": "already_connected"})

    # Request already pending
    if existing and existing.status == "pending":
        return JsonResponse({"status": "already_sent"})

    # Rejected earlier 
    if existing and existing.status == "rejected":
        existing.status = "pending"
        existing.save()
        return JsonResponse({"status": "resent"})

    # No previous request
    ConnectionRequest.objects.create(
        sender=request.user,
        receiver=receiver,
        status="pending"
    )

    return JsonResponse({"status": "sent"})

# follow
@login_required
def follow_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    data = json.loads(request.body)
    user_id = data.get("user_id")

    if int(user_id) == request.user.id:
        return JsonResponse({"error": "Cannot follow yourself"}, status=400)

    user_to_follow = User.objects.get(id=user_id)

    Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )

    return JsonResponse({"status": "followed"})





# incoming_requests page
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@never_cache
@login_required
def incoming_requests(request):
    requests = ConnectionRequest.objects.filter(
        receiver=request.user,
        status="pending"
    )
    return render(
        request,
        "Connections/incoming_requests.html",
        {"requests": requests}
    )

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def respond_request_ajax(request):
    req_id = request.POST.get("req_id")
    action = request.POST.get("action")

    if not req_id or not action:
        return JsonResponse(
            {"error": "Invalid data"},
            status=400
        )

    req = ConnectionRequest.objects.filter(
        id=req_id,
        receiver=request.user,
        status="pending"
    ).first()

    if not req:
        return JsonResponse(
            {"error": "Request not found or already handled"},
            status=404
        )

    if action == "accept":
        req.status = "accepted"
        req.save()
        return JsonResponse({"status": "accepted"})

    if action == "reject":
        req.status = "rejected"
        req.save()
        return JsonResponse({"status": "rejected"})

    return JsonResponse(
        {"error": "Invalid action"},
        status=400
    )

# disconnection
from django.db.models import Q

@login_required
def disconnect_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    data = json.loads(request.body)
    user_id = data.get("user_id")

    if not user_id:
        return JsonResponse({"error": "Missing user_id"}, status=400)

    other_user = User.objects.get(id=user_id)

    # DELETE accepted connection in BOTH directions
    deleted, _ = ConnectionRequest.objects.filter(
        status="accepted"
    ).filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).delete()


    if deleted == 0:
        return JsonResponse(
            {"error": "No active connection found"},
            status=404
        )

    return JsonResponse({"status": "disconnected"})

# unfollow

@login_required
def unfollow_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    data = json.loads(request.body)
    user_id = data.get("user_id")

    if not user_id:
        return JsonResponse({"error": "Missing user_id"}, status=400)

    Follow.objects.filter(
        follower=request.user,
        following_id=user_id
    ).delete()

    return JsonResponse({"status": "unfollowed"})


# connection list
from django.db.models import Q

@login_required
def connections_list(request):
    connections = ConnectionRequest.objects.filter(
        status="accepted"
    ).filter(
        Q(sender=request.user) | Q(receiver=request.user)
    )

    connected_users = []
    for conn in connections:
        if conn.sender == request.user:
            connected_users.append(conn.receiver)
        else:
            connected_users.append(conn.sender)

    return render(
        request,
        "Connections/connections_list.html",
        {"users": connected_users}
    )


# followers_list

@login_required
def followers_list(request):
    followers = Follow.objects.filter(
        following=request.user
    ).select_related("follower")

    return render(
        request,
        "Connections/followers.html",
        {"followers": followers}
    )
