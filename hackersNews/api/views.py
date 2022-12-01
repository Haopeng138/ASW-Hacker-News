from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import UserAPIKey
from accounts.models import HNUser
from homepage.models import *
from .serializers import *
import json
from django.db.utils import IntegrityError
# Create your views here.

# Indica que model usar para las API Keys
class HasAPIKey(BaseHasAPIKey):
    model = UserAPIKey

# USER

def getUser(id):
    try:
        return HNUser.objects.get(pk=id)
    except:
        print("ID not found, trying as key")
        try:
            return HNUser.objects.get(key=id)
        except:
            raise Http404

"""
@csrf_exempt
@api_view(['GET','POST','PUT'])
@permission_classes([HasAPIKey])
# Deprecado
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
"""

class user_list(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request, format=None):
        users = HNUser.objects.all()
        serializer = HNUserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, fomat=None):
        data = JSONParser().parse(request)
        newUser = HNUserSerializer.create(HNUserSerializer, validated_data=data)
        if newUser is not None:
            serializer = HNUserSerializer(newUser, many=False)
            return JsonResponse(serializer.data)
        return JsonResponse(data,status=400)

"""
@permission_classes([HasAPIKey])
def users_list(request):
    key = request.META["HTTP_AUTHORIZATION"].split()[1]
    #api_key = UserAPIKey.objects.get_from_key(key)
    user = HNUser.objects.get(key=key)
    if request.method == 'GET':
        users = HNUser.objects.all()
        serializer = HNUserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
"""

class user_detail(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request, id, format=None):
        user = getUser(id)

        serializer = HNUserSerializer(user)
        return JsonResponse(serializer.data)

    def put(self, request, id, format=None):
        user = getUser(id)
        serializer = HNUserSerializer(user, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

class user_comments(APIView):
    permission_classes = [HasAPIKey]

    def user_comments(self, user):
        user_comments = Comment.objects.filter(user=user)
        serializer = CommentSerializer(user_comments, many=True)
        return JsonResponse(serializer.data, safe=False)

    def upvoted_comments(self, user):
        upvoted_comments = Comment.objects.filter(commentvotetracking__user=user)
        serializer = CommentSerializer(upvoted_comments, many=True)
        return  JsonResponse(serializer.data, safe=False)

    def get(self, request, id, format=None):
        user = getUser(id)

        upvoted = request.GET.get('u', '0')

        if upvoted == '0':
            return self.user_comments(user)
        else:
            return self.upvoted_comments(user)


"""
@permission_classes([HasAPIKey])
def get_user_comments(request, id):
    if request.method == 'GET':
        user = HNUser.objects.get(pk=id)
        user_comments = Comment.objects.filter(user=user)
        serializer = CommentSerializer(user_comments, many=True)
        return JsonResponse(serializer.data, safe=False)
"""

class user_submissions(APIView):
    permission_classes = [HasAPIKey]

    def user_submissions(self, user):
        user_submissions = Post.objects.filter(user=user)
        serializer = PostSerializer(user_submissions, many=True)
        return JsonResponse(serializer.data, safe=False)

    def upvoted_submission(self, user):
        upvoted_submissions = Post.objects.filter(upvotes__user=user)
        serializer = PostSerializer(upvoted_submissions, many=True)
        return JsonResponse(serializer.data, safe=False)

    def get(self, request, id, format=None):
        user = getUser(id)

        upvoted = request.GET.get('u', '0')

        if upvoted == '0':
            return self.user_submissions(user)
        else:
            return self.upvoted_submission(user)


"""
@permission_classes([HasAPIKey])
def get_user_submissions(request, id):
    if request.method == 'GET':
        user = User.objects.get(pk=id)
        user_submissions = Post.objects.filter(user=user)
        serializer = PostSerializer(user_submissions, many=True)
        return JsonResponse(serializer.data, safe=False)
"""

# SUBMISSION

class submission_list(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request, format=None):

        submissions = Post.objects.all()
        serializer = PostSerializer(submissions, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        user = getUser(key)
        data = JSONParser().parse(request)
        print(data)
        serializer = PostSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save(user=user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def post_list(request):
    if (request.method == 'GET'):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

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

def get_submission_list(request):
    pass






# UPVOTE
@permission_classes([HasAPIKey])
@csrf_exempt
def upvote_post(request,id):
    return upvote(request, 'post',id)

@permission_classes([HasAPIKey])
@csrf_exempt
def upvote_comment(request,id):
    return upvote(request, 'comment',id)

@api_view(['POST'])
@permission_classes([HasAPIKey])
@csrf_exempt
def upvote(request, item_str,id):
    key = request.META["HTTP_AUTHORIZATION"].split()[1]
    user = getUser(key)
    print(user.id)
    if request.method == 'POST':
        if user.id:
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
                return JsonResponse({'success': False,'message':'Ya has votado'})

            return JsonResponse({'success': True,'message':'Votado con existo'})
        else: return JsonResponse({'success': False,'message':'No user'})

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

@permission_classes([HasAPIKey])
@csrf_exempt
def unvote(request, item_str,id):
    key = request.META["HTTP_AUTHORIZATION"].split()[1]
    user = getUser(key)
    print(user.id)
    if request.method == 'POST':
        print(user.id)
        if user.id:
            if item_str == 'post':
                item = Post.objects.filter(id=id)[0]
                PostVoteTracking.objects.filter(user=user, post=item).delete()
            else:
                print("some")
                print(user.id)
                item = Comment.objects.filter(id=id)[0]
                CommentVoteTracking.objects.filter(user=user, comment=item).delete()
            try:

                item.user.karma -= 1
                item.user.save()
                item.votes -= 1
                item.save()
            except IntegrityError:
                return JsonResponse({'success': False,'message':'No habias votado'})

            return JsonResponse({'success': True,'message':'Has desvotado'})
        else: return JsonResponse({'success': False,'messafe':'No user'})


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