from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework_api_key.permissions import HasAPIKey
from .models import UserAPIKey
from accounts.models import HNUser
from.serializers import HNUserSerializer
from homepage.models import *
import json
from django.db.utils import IntegrityError
# Create your views here.
@csrf_exempt
@api_view(['GET','POST'])
@permission_classes([HasAPIKey])
def user(request, id):
    key = request.META["HTTP_AUTHORIZATION"].split()[1]

    if id is not None:
        try:
            user = HNUser.objects.get(pk=id)
        except HNUser.DoesNotExsist:
            return HttpResponse(satus=404)

    else:
        try:
            user = HNUser.objects.get(pk=id)
        except HNUser.DoesNotExsist:
            return HttpResponse(satus=404)

    if request.method == 'GET':
        serializer = HNUserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = HNUserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    return HttpResponse(status=400)

@permission_classes([HasAPIKey])
def users_list(request):
    print(request.META)
    key = request.META["HTTP_AUTHORIZATION"].split()[1]
    api_key = APIKey.objects.get_from_key(key)
    user = HNUser.objects.get(api_key=api_key)
    print(user.id)
    if request.method == 'GET':
        users = HNUser.objects.all()
        serializer = HNUserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)



#@permission_classes([HasAPIKey])
@csrf_exempt
def upvote_post(request,id):
    print(request.headers)
    return upvote(request, 'post',id)


@permission_classes([HasAPIKey])
@csrf_exempt
def upvote_comment(request,id):
    return upvote(request, 'comment',id)

@api_view(['POST'])
#@permission_classes([HasAPIKey])
@csrf_exempt
def upvote(request, item_str,id):
    key = request.META["HTTP_AUTHORIZATION"].split()[1]
    api_key = APIKey.objects.get_from_key(key)
    user = HNUser.objects.get(api_key=api_key)
    print(user.id)
    if request.method == 'POST':
        print(request.headers)
        print(request.headers['Apikey'])
        user = UserAPIKey.objects.get_from_key(request.headers['Apikey'])
        print(user.id)
        if user.id:
            user = HNUser.objects.filter(id=user.id)[0]
            if item_str == 'post':
                item = Post.objects.filter(id=id)[0]
                tracking = PostVoteTracking(user=user, post=item)
            else:
                item = Comment.objects.filter(id=id)[0]
                tracking = CommentVoteTracking(user=user, comment=item)
            try:
                tracking.save()
                item.user.karma += 1
                item.user.save()
                item.votes += 1
                item.save()
            except IntegrityError:
                return JsonResponse({'success': False})

            return JsonResponse({'success': True})
        else: return JsonResponse({'success': False})

@api_view(['POST'])
@permission_classes([HasAPIKey])
@csrf_exempt
def unvote_post(request,id):
    return unvote(request, 'post',id)

@api_view(['POST'])
@permission_classes([HasAPIKey])
@csrf_exempt
def unvote_comment(request,id):
    return unvote(request, 'comment',id)

@csrf_exempt
def unvote(request, item_str,id):
    if request.method == 'POST':

        if request.user.id:
            user = HNUser.objects.filter(id=request.user.id)[0]
            if item_str == 'post':
                item = Post.objects.filter(id=id)[0]
                print("Imprimiendo")
                print(PostVoteTracking(user=user, post=item))
                PostVoteTracking.objects.filter(user=user, post=item).delete()
            else:
                item = Comment.objects.filter(id=id)[0]
                CommentVoteTracking.objects.filter(user=user, comment=item).delete()
            try:

                item.user.karma -= 1
                item.user.save()
                item.votes -= 1
                item.save()
            except IntegrityError:
                return JsonResponse({'success': False})

            return JsonResponse({'success': True})
        else: return JsonResponse({'success': False})

@permission_classes([HasAPIKey])
def sub_comment_list(request, id):
    if request.method == 'GET':
        submission = Post.objects.get(pk=id)
        comment_list = submission.comment_set
        serializer = CommentSerializer(comment_list, many=True)
        return JsonResponse(serializer.data, safe=False)

@permission_classes([HasAPIKey])
def get_submission(request, id):
    if request.method == 'GET':
        submission = Post.objects.get(pk=id)
        serializer = PostSerializer(submission, many=False)
        return JsonResponse(serializer.data, safe=False)

@permission_classes([HasAPIKey])
def get_user_comments(request, id):
    if request.method == 'GET':
        user = User.objects.get(pk=id)
        user_comments = Comment.objects.filter(user=user)
        serializer = CommentSerializer(user_comments, many=True)
        return JsonResponse(serializer.data, safe=False)

@permission_classes([HasAPIKey])
def get_user_submissions(request, id):
    if request.method == 'GET':
        user = User.objects.get(pk=id)
        user_submissions = Post.objects.filter(user=user)
        serializer = PostSerializer(user_submissions, many=True)
        return JsonResponse(serializer.data, safe=False)

@permission_classes([HasAPIKey])
def post_comment(request, id):
    post = Post.objects.get(pk=id)
    if request.method == 'GET':
        serializer = PostSerializer(post, many=False)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        content = request.POST['text'].strip()
        comment = Comment(user=request.user,
                          post=post,
                          reply=None,
                          content=content)
        serializer = CommentSerializer(comment, many=False)
        return JsonResponse(serializer.data, safe=False)