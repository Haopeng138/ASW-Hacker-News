from django.contrib import admin
from .models import *
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(VoteTracking)
admin.site.register(PostVoteTracking)
admin.site.register(CommentVoteTracking)