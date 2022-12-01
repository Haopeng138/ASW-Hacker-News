from django.utils import timezone
from email.policy import default
from statistics import mode
from time import time
from django.db import models
from urllib.parse import urlparse
from accounts.models import HNUser
from django.urls import reverse

### Miguel:

def parse_site(url):
    if url:
        netloc = urlparse(url).netloc.split('.')
        return f'{netloc[-2]}.{netloc[-1]}'
    else:
        return None


def time_from(dt):
    lapse = timezone.now() - dt
    days = lapse.days
    hours, remainder = divmod(lapse.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return f'{days:.0f} days ago'
    elif hours > 0:
        return f'{hours:.0f} hours ago'
    elif hours == 0:
        return f'{minutes:.0f} minutes ago'
    else:
        raise ValueError

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    @property
    def time_from_post(self):
        return time_from(self.insert_date)

    title = models.CharField(null=False,max_length=255)
    url = models.CharField(null=True,max_length=255)
    site = models.CharField(null=True,max_length=255)
    votes = models.IntegerField(default=0)
    user = models.ForeignKey(to=HNUser, on_delete=models.CASCADE)
    insert_date = models.DateTimeField(null=False)
    comments = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.site = parse_site(self.url)
        if not self.insert_date:
            self.insert_date = timezone.now()
        super().save(*args, **kwargs)
"""
        class VoteTracking(models.Model):
             insert_date = models.DateTimeField(null=False)

    def save(self, *args, **kwargs):
        if not self.insert_date:
            self.insert_date = timezone.now()
        super().save(*args, **kwargs)
"""

class VoteTracking(models.Model):
    insert_date = models.DateTimeField(null=False)
    def save(self, *args, **kwargs):
        if not self.insert_date:
            self.insert_date = timezone.now()
        super().save(*args, **kwargs)

class PostVoteTracking(VoteTracking):
    user = models.ForeignKey(to=HNUser, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, related_name="upvotes", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + '_' + self.post.title

    class Meta:
        unique_together = (('user','post'),)

class Comment(models.Model):
    @property
    def time_from_post(self):
        return time_from(self.insert_date)

    insert_date = models.DateTimeField(null=False)
    content = models.TextField(null=False)
    user = models.ForeignKey(to=HNUser, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True)
    votes = models.IntegerField(default=1)

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        if not self.insert_date:
            self.insert_date = timezone.now()
        super().save(*args, **kwargs)

class CommentVoteTracking(VoteTracking):
    user = models.ForeignKey(to=HNUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + '_' + self.comment.content

    class Meta:
        unique_together = (('user', 'comment'),)
