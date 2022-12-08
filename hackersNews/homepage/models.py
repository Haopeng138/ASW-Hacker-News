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

# NO SE COMO VA ESTO??
def check_submission(title, url):
    if not title or title == '':
        return False
    elif not url:
        return False
    try:
        if (parse_site(url) is None): return False
        return True
    except IndexError:
        return False



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

class PostManager(models.Manager):
    def create(self, title, userID, url=None, text=None):
        print("Creating Post")
        if url is not None:
            if Post.objects.filter(url = url).exists() and url != '':
                # URL REPETIDA
                print("Url repetida")
                return None
                
            if not check_submission(title, url):
                print("URL Incorrecta")
                # URL INCORRECTA
                return None

        user = HNUser.objects.get(pk=userID)

        newPost = Post(title=title, url=url, site=parse_site(url), user=user, insert_date=timezone.now())
        
        newPost.save()
        
        if (url is None or url == ''):
            newPost.text=text
        else:
            Comment.objects.create(content=text, user=user, post=newPost)


class Post(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(null=False,max_length=255)
    url = models.CharField(null=True,max_length=255)
    site = models.CharField(null=True,max_length=255)
    text = models.CharField(null=True, max_length=1024)
    
    @property
    def votes(self):
        return PostVoteTracking.objects.filter(post=self).count()

    user = models.ForeignKey(to=HNUser, on_delete=models.CASCADE)
    
    @property
    def time_from_post(self):
        return time_from(self.insert_date)

    insert_date = models.DateTimeField(null=False)

    @property
    def numComments(self):
        return Comment.objects.filter(post=self).count()

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.site = parse_site(self.url)
        if not self.insert_date:
            self.insert_date = timezone.now()
        super().save(*args, **kwargs)

class CommentManager(models.Manager):

    pass

class Comment(models.Model):
    @property
    def time_from_post(self):
        return time_from(self.insert_date)

    insert_date = models.DateTimeField(null=False)
    content = models.TextField(null=False)
    user = models.ForeignKey(to=HNUser, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=False)
    reply = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True)
    
    @property
    def votes(self):
        return CommentVoteTracking.objects.filter(Comment=self).count()

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        if not self.insert_date:
            self.insert_date = timezone.now()
        super().save(*args, **kwargs)

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

class CommentVoteTracking(VoteTracking):
    user = models.ForeignKey(to=HNUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(to=Comment, related_name="upvotes", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + '_' + self.comment.content

    class Meta:
        unique_together = (('user', 'comment'),)
