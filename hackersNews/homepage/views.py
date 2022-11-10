import django.contrib.auth
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import *
from urllib.parse import urlparse
from django.contrib.auth import get_user_model, authenticate
from accounts.models import HNUser
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
import json
import logging
from django.db.utils import IntegrityError
from datetime import timedelta

## Pagina principal 
def testindex(request,page=None):
  template = loader.get_template('index.html')
  posts = Post.objects.all()
  context = {
     'post' : posts
  }
  return HttpResponse(template.render(None,request))

def check_submission(title, url, text):
    if not title:
        return False
    elif title == '':
        return False
    elif not url and not text:
        return False
    elif url:
        try:
            parse_site(url)
            return True
        except IndexError:
            return False
    else:
        return True

def login(request):		 
   template = loader.get_template('registration/login.html')		    
   return HttpResponse(template.render(None,request))

def submit(request):
    if request.method == 'POST':

        title = request.POST['title'].strip()
        url = request.POST['url']
        text = request.POST['text'].strip()

        if not check_submission(title, url, text):
            return render(request, 'post/submit.html', context={'errors': True})

        user = request.user
        user.save()

        current_post = Post(title=title, url=url, user=user)
        current_post.save()

        log.info(f'Post {title} submitted')

        # if text:
        #     current_comment = Comment(content=text, user=user, post=current_post)
        #     current_comment.save()

        return redirect('new')

    else:
        return render(request, 'post/submit.html')



@csrf_exempt
def create(request):
  usr = request.POST['acct']
  pwd = request.POST['pw']
  newUser = Login(username=usr, password = pwd)
  newUser.save()
  output = "Create Usr: " + usr + " Pw: " + pwd
  print(output)
  return HttpResponse(testIndex(request))

# def login(request):
#   usr = request.POST['acct']
#   pwd = request.POST['pw']

#   output = "Usr: " + usr + " Pw: " + pwd
#   print(output)
#   return HttpResponse(output,request)

def logout(request):
  
  return redirect('/')


def testIndex(request):
  myusers = Login.objects.all().values()
  template = loader.get_template('testUsr.html')
  context = { 'myusers' : myusers, }
  return HttpResponse(template.render(context, request))


def account(request):
  # return redirect('/account/',permanent=True)
  userModel = get_user_model()
  print("He llegado aqui")
  #userModel = hackersNews.accounts.models.HNUser
  if request.POST.get('submit')=='Sign Up':
    print("Sign up")
    username=request.POST.get('username')
    email=request.POST.get('email')
    password=request.POST.get('pw')

    if userModel.objects.filter(email=email).exists():                             # Condition for same email id if already exists
      messages.warning(request,'Email already exists')
    else:
      user =userModel.objects.create_user(email=email,password=password,username=username)
      user.set_password(password)                                             #since raw passwords are not saved therefore needs to set in this method
      user.save()
      messages.success(request,'User has been registered successfully')      #Dispalys message that user has been registerd
      django.contrib.auth.login(request, user)
    return redirect('/homepage/account')

  elif request.POST.get('submit')=='Log in':
    print("Login")
    email = request.POST['email']
    password = request.POST['pw']

    user = authenticate(request, email=email, password=password)
    print(user)
    if user is not None:
      django.contrib.auth.login(request, user)
      return redirect ('/')
    else:
      messages.warning(request,'Invalid credentials')
  # print(email,password,username)

  return render(request,'testLogin.html')


# def testProfile(request):
#   template = loader.get_template('user/profile.html')
#   context = {
#     'username': 'hao',
#     'karma': 3, 
#     'email': 'hao@gmail.com',
#     'about': 'Mucho texto',
#     'own_user': True
#   }
#   return HttpResponse(template.render(context, request))

def profile(request, user_id):
    #log.info(f'Loading profile {user_id}...')
    user_query = HNUser.objects.filter(id=user_id)

    if user_query:
        user = user_query[0]

        if user.id == request.user.id:
            context = {
                'user_id': user_id,
                'username': user.username,
                'karma': user.karma,
                'about': user.about,
                'email': user.email,
                'own_user': True
            }
        else:
            context = {
                'user_id': user_id,
                'username': user.username,
                'karma': user.karma,
                'about': user.about,
                'own_user': False
            }
        return render(request, 'user/profile.html', context=context)
    else:
        return redirect('index')

def validate_user_email(email):
    try:
        validate_email(email)
        return True
    except :
        
        return False

def send_confirmation_email(user):
    confirmation_email_text = f"""Hi {user.username},\n\nHo"""
    send_mail(
        subject=f'Confirmation email from Hacker Newst',
        message=confirmation_email_text,
        from_email='info@datatau.net',
        recipient_list=[user.email],
        fail_silently=False
    )

def update_profile(request, user_id):
    if request.method == 'POST':
        body = request.POST

        updated_profile = False

        user = request.user
        if 'about' in body:
            user.about = body['about']
            updated_profile = True

        invalid_email = True
        if 'email' in body and validate_user_email(body['email']):
            user.email = body['email']
            #user.is_active = False

            user.save()

            #send_confirmation_email(user)

            #return HttpResponse(
                #"<h1>Email successfully updated!</h1><p>We've just sent you a confirmation email. Please check your inbox and click on the confirmation link :)</p>")

        user.save()

  

        context = {
            'user_id': user_id,
            'username': user.username,
            'karma': user.karma,
            'about': user.about,
            'email': user.email,
            'invalid_email': invalid_email,
            'updated_profile': updated_profile,
            'own_user': True
        }
        return render(request, 'user/profile.html', context=context)

def testPost(request):
  current_post ={
    'title': "Titulo random",
    'id': 45342,
    'user': {
      'username':'hao',
      'id': 3,
    },
    'url': "some@gmail.com",
    'side': 'www.google.com',
    'votes':4,
    'time_from_post': 1341,

  }

  posttracking = [
    45352
  ]
  context = {'post': current_post,
            'post_tracking': posttracking,
            'tracking': 3243,
            'root_comments': 4324,
            'error': True}
  return render(request,'post/post.html',context)

def testSubmitPost(request):
  context = {
    'error':False
  }
  return render(request,'post/submit.html',context)

def testPostEdit(request):
  current_post ={
  'title': "Titulo random",
  'id': 45342,
  'user': {
    'username':'hao',
    'id': 3,
  },
  'url': "some@gmail.com",
  'site': 'www.google.com',
  'votes':4,
  'time_from_post': 1341,
  }
  context = {
    'post':current_post,
    
  }
  return render(request,'post/post_edit.html',context)

# Haciendo merge manual de la rama de miguel

def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


log = get_logger()

def get_tracking(user, items):
    if user.id:
        if len(items) > 0:
            is_post = isinstance(items[0], Post)
            log.info(f'checking tracking for {"posts" if is_post else "comments"}...')
            if is_post: return [x.post.id for x in PostVoteTracking.objects.filter(user__id=user.id)]
            else: return [x.comment.id for x in CommentVoteTracking.objects.filter(user__id=user.id)]
    return []

def render_index_template(request, posts, tracking, category, page, additional_context=None):
    context = {
        'posts': posts,
        'tracking': tracking,
        'page': page +1,
        'category': category,
        'counter_init': settings.PAGE_LIMIT * (page -1)
    }
    if additional_context: context.update(additional_context)
    return render(request, template_name='index.html', context=context)

def get_page(page):
    if page: return page
    else: return 1

def post_sort_key(post_object):
    n_upvotes = post_object.votes
    score = (n_upvotes)
    return score

def get_hottest(page):
    now = timezone.now()
    all_posts = Post.objects.all()
    return sorted(all_posts, key=post_sort_key, reverse=True)[(page - 1) * settings.PAGE_LIMIT:settings.PAGE_LIMIT * page]

def index(request, page=None):
    page = get_page(page)
    posts = get_hottest(page)
    tracking = get_tracking
    return render_index_template(request, posts, tracking, '', page)

def check_submission(title, url, text):
    if not title:
        return False
    elif title == '':
        return False
    elif not url and not text:
        return False
    elif url:
        try:
            parse_site(url)
            return True
        except IndexError:
            return False
    else: return True

def submission(request):
    if request.method == 'POST':
        title = request.POST['title'].strip()
        url = request.POST['url']
        text = request.POST['text'].strip()

        if not check_submission(title, url, text):
            return render(request, 'post/submission.html', context={'errors': True})
        user = request.user
        user.save()
        current_post = Post(title=title, url=url, user=user)
        current_post.save()
        log.info(f'Post {title} submitted')

        if text:
            current_comment = Comment(content=text, user=user, post=current_post)
            current_comment.save()
        return redirect('new')
    else: return render(request, 'post/submission.html')

def post(request, post_id, error=None):
    if request.method == 'GET':
        current_post = Post.objects.get(pk=post_id)
        log.info(f'retrieved post {post_id}')
        current_comments = current_post.comment_set.filter(reply=None).order_by('insert_date')
        log.info(f'retrieved {len(current_comments)} comment(s) for post {current_post.id}')
        context = {
            'post': current_post,
            'post_tracking': get_tracking(request.user, [current_post]),
            'tracking': get_tracking(request.user, current_comments),
            'root_comments': current_comments,
            'error': error
        }
        return render(request, 'posts/post.html', context=context)
    else: return HttpResponse('ERROR')

def post_edit(request, post_id, errors=False):
    current_post = Post.objects.get(pk=post_id)
    if request.user != current_post.user:
        log.info(f'user {request.user.id} is not allowed to edit post {post_id}')
        return redirect('post', post_id=post_id)
    if request.method == 'GET':
        context = {'post': current_post}
        if errors: context.update({'errors': True})
        return render(request, 'post/post_edit.html', context=context)
    elif request.method == 'POST':
        title = request.POST['title'].strip()
        if title == '':
            request.method = 'GET'
            return post_edit(request=request, post_id=post_id, errors=True)
        else:
            current_post.title = title
            current_post.save()
            log.info(f'post {post_id} edited')
            return redirect('post', post_id=current_post.id)

def post_delete(request, post_id, errors=False, deleted=False):
    current_post = Post.objects.get(pk=post_id)
    if request.user != current_post.user:
        log.info(f'user {request.user.id} is not allowed to delete post {post_id}')
        return redirect('post', post_id=post_id)
    if request.method == 'GET':
        if not deleted:
            context = {'post': current_post, 'errors': errors}
            return render(request, 'post/post_delete.html', context=context)
        else:
            current_post.delete()
            log.info(f'post {post_id} deleted')
            context = {'deleted': deleted}
            return render(request, 'post/post_delete.html', context=context)
    elif request.method == 'POST':
        delete = request.POST['delete']
        if delete == 'Yes':
            try:
                request.method = 'GET'
                return post_delete(request, post_id, errors=False, deleted=True)
            #except Excepton as ex:
            except:
                ex = "random"
                log.error(ex)
                log.info(f'unable to delete post {post_id}')
                request.method = 'GET'
                return post_delete(request, post_id, errors=True, deleted=False)
        else:
            request.method = 'GET'
            return post_edit(request=request, post_id=post_id)

@csrf_exempt
def upvote_post(request):
    return upvote(request, 'post')
    
@csrf_exempt
def upvote(request, item_str):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        log.info(f'Upvote {item_str}')
        if request.user.id:
            user = HNUser.objects.filter(id=request.user.id)[0]
            if item_str == 'post':
                item = Post.objects.filter(id=body['id'])[0]
                tracking = PostVoteTracking(user=user, post=item)
            else:
                item = Comment.objects.filter(id=body['id'])[0]
                tracking = CommentVoteTracking(user=user, comment=item)
            try:
                tracking.save()
                item.user.karma += 1
                item.user.save()
                item.votes += 1
                item.save()
            except IntegrityError:
                return JsonResponse({'success': False, 'redirect': False})

            return JsonResponse({'success': True, 'redirect': False})
        else: return JsonResponse({'success': False, 'redirect': True})

def hackernews (request, page=None):
    if request.method == 'GET':
        page = get_page(page)
        posts = Post.objects. \
            order_by('votes')[(page - 1) * settings.PAGE_LIMIT:settings.PAGE_LIMIT * page]
        tracking = get_tracking(request.user, posts)
        return render_index_template(request, posts, tracking, 'new', page)

def new (request, page=None):
    if request.method == 'GET':
        page = get_page(page)
        posts = Post.objects. \
            order_by('-insert_date')[(page - 1) * settings.PAGE_LIMIT:settings.PAGE_LIMIT * page]
        tracking = get_tracking(request.user, posts)
        return render_index_template(request, posts, tracking, 'new', page)