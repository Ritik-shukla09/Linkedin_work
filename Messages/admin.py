from django.contrib import admin
from .models import Chat, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("chat", "sender", "timestamp")
    list_filter = ("timestamp",)
