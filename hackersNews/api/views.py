from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework_api_key.permissions import HasAPIKey
from .models import UserAPIKey
from accounts.models import HNUser
from.serializers import HNUserSerializer
from homepage.models import *

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
    if request.method == 'GET':
        users = HNUser.objects.all()
        serializer = HNUserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

@permission_classes([HasAPIKey])
def sub_comment_list(request, id):
    if request.method == 'GET':
        submission = Post.objects.filter(pk=id)
        comment_list = submission.comment_set
        serializer = CommentSerializer(comment_list, many=True)
        return JsonResponse(serializer. data, safe=False)

def get_submission(request, id):
    if request.method == 'GET':
        submission = Post.objects.filter(pk=id)
        serializer = PostSerializer(submission, many=False)
        return JsonResponse(serializer.data, safe=False)