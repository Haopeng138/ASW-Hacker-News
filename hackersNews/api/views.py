from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import UserAPIKey
from accounts.models import HNUser
from homepage.models import *
from .serializers import *
from django.db.utils import IntegrityError
from rest_framework import exceptions
from rest_framework import status

# Indica que model usar para las API Keys
class HasAPIKey(BaseHasAPIKey):
    model = UserAPIKey

### --- HELPER FUNCTIONS --- ####
def get_fields_from_request(request):
    """ Returns list of fields from query parametes"""
    try:
        fields = request.GET.get('fields', None)
        if fields == '': fields = None
        fields = fields.split(',')
    except:
        fields=None
    return fields

def filter_by_id_from_request(request,query_set):
    try:
        id = request.GET.get('id',None)
        if id == '' or id is None: return query_set
        id = id.split(',')
        return query_set.filter(id__in=id)
    except: 
        print("EXCEPTION in Filter by ids")
        return query_set

def string_to_bool(string:str) -> bool:
    return string.lower() in ['true', 'yes', '1', 't']


    #    USER     #

def getUserFromID(id) -> HNUser:
    try:
        return HNUser.objects.get(pk=id)
    except:
        raise exceptions.NotFound("User with ID: {id} was not found")

def getUserFromKey(key) -> HNUser:
    try:
        return HNUser.objects.get(key=key)
    except:
        if key is None: raise exceptions.NotAuthenticated(detail="Authorization key was not found")
        raise exceptions.APIException(detail="Api-Key has no user associated", code=status.HTTP_410_GONE)
           
def getUserFromRequest(request) -> HNUser:
    key = request.META["HTTP_AUTHORIZATION"].split()[1]
    return getUserFromKey(key)

class user_list(APIView):
    permission_classes = []

    def get(self, request, format=None):
        fields = get_fields_from_request(request)

        users = HNUser.objects.all()
        users = filter_by_id_from_request(request=request, query_set=users)
        
        serializer = HNUserSerializer(users, fields=fields, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def post(self, request, fomat=None):
        data = JSONParser().parse(request)
        serializer = HNUserSerializer(data=data)

        if serializer.is_valid():
            newUser = serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(data,status=status.HTTP_400_BAD_REQUEST)

class user_detail(APIView):
    # permission_classes = [HasAPIKey]
    http_method_names = ["GET", "PUT"]

    def get(self, request, id, format=None):
        user = getUserFromID(id)
        fields = get_fields_from_request(request)

        serializer = HNUserSerializer(user, fields=fields)
        return JsonResponse(serializer.data)

    def put(self, request, id, format=None):
        user = getUserFromID(id)
        key_user = getUserFromRequest(request)

        if user != key_user: raise exceptions.PermissionDenied("Cannot update other user's info")
        
        data = JSONParser().parse(request)
        serializer = HNUserSerializer(user, data=data)
        
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        
        return JsonResponse(serializer.errors, status=400)

class user_comments(APIView):
    permission_classes = [HasAPIKey]
    http_method_names = ["GET"]

    def user_comments(self, user):
        user_comments = Comment.objects.filter(user=user)
        serializer = CommentSerializer(user_comments, many=True)
        return JsonResponse(serializer.data, safe=False)

    def upvoted_comments(self, user):
        upvoted_comments = Comment.objects.filter(commentvotetracking__user=user) # Renamed to upvotes__user??
        serializer = CommentSerializer(upvoted_comments, many=True)
        return  JsonResponse(serializer.data, safe=False)

    def get(self, request, id, format=None):
        user = getUserFromID(id)

        upvoted = string_to_bool(request.GET.get('upvoted', 'False'))

        if upvoted:
            if user != getUserFromRequest(request): raise exceptions.PermissionDenied("Cannot view other user's upvoted comments")
            return self.upvoted_comments(user)
        else:
            return self.user_comments(user)

class user_submissions(APIView):
    permission_classes = [HasAPIKey]
    http_method_names = ["GET"]

    def user_submissions(self, user):
        user_submissions = Post.objects.filter(user=user)
        serializer = PostSerializer(user_submissions, many=True)
        return JsonResponse(serializer.data, safe=False)

    def upvoted_submission(self, user):
        upvoted_submissions = Post.objects.filter(upvotes__user=user)
        serializer = PostSerializer(upvoted_submissions, many=True)
        return JsonResponse(serializer.data, safe=False)

    def get(self, request, id, format=None):
        user = getUserFromID(id)

        #upvoted = request.GET.get('upvoted', 'False')
        upvoted = string_to_bool(request.GET.get('upvoted', 'False'))


        if upvoted:
            if user != getUserFromRequest(request): raise exceptions.PermissionDenied("Cannot view other user's upvoted submissions")
            return self.upvoted_submission(user)
        else:
            return self.user_submissions(user)

    #  SUBMISSION  #

def get_submisison_from_id(id) -> Post:
    try:
        return Post.objects.get(id=id)
    except:
        raise exceptions.NotFound("Submission with ID: {id} was not found")

class submission_list(APIView):
    # permission_classes = [HasAPIKey]

    def order_query_set(self, posts, field:str, ascending=False):
        if field is None: return posts.order_by('-insert_date')
        if not ascending: field='-'+ field
        posts = posts.order_by(field)
        return posts

    def get(self, request, format=None):
        fields = get_fields_from_request(request)
        order_by = request.GET.get('order_by',None)
        ascending = string_to_bool(request.GET.get('ascending', 'false'))

        submissions = Post.objects.all()
        submissions = self.order_query_set(submissions,order_by,ascending)
        submissions = filter_by_id_from_request(request, submissions)
        
        serializer = PostSerializer(submissions, fields=fields, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        user = getUserFromRequest(request)

        data = JSONParser().parse(request)
        
        print(data)

        serializer = PostSerializer(data=data)
        if (serializer.is_valid()):
            serializer.save(user=user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=400)

class submission_detail(APIView):
    http_method_names = ["GET"]

    def get(self, request, id, format=None):
        fields = get_fields_from_request(request)
        submission = get_submisison_from_id(id)
        serializer = PostSerializer(submission, fields=fields)
        return JsonResponse(serializer.data, stauts = status.HTTP_200_OK)

class submission_comments(APIView):
    http_method_names = ["GET", "POST"]
    
    def get(self, request, id, format=None):
        submission = get_submisison_from_id(id)
        comment_list = submission.comment_set
        serializer = CommentSerializer(comment_list, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, id, format=None):
        user = getUserFromRequest(request)
        submission = get_submisison_from_id(id)

        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)

        if (serializer.is_valid()):
            serializer.save(user=user)
            serializer.save(post=submission)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## DEPRECADO - submission_comments
@permission_classes([HasAPIKey])
@csrf_exempt
def sub_comment_list(request, id):
    print(request)
    submission = Post.objects.get(pk=id)
    if request.method == 'GET':
        comment_list = submission.comment_set
        serializer = CommentSerializer(comment_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        """
        content = request.POST['text'].strip()
        comment = Comment(user=request.user,
                          post=post,
                          reply=None,
                          content=content)
        serializer = CommentSerializer(comment, many=False)
        return JsonResponse(serializer.data, safe=False)
        """
        user = getUserFromRequest(request)
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if (serializer.is_valid()):
            serializer.save(user=user)
            serializer.save(post=submission)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

## DEPRECADO - submission_detail
@permission_classes([HasAPIKey])
def get_submission(request, id):
    if request.method == 'GET':
        submission = Post.objects.get(pk=id)
        serializer = PostSerializer(submission, many=False)
        return JsonResponse(serializer.data, safe=False)

# UPVOTE
@csrf_exempt
@api_view(['POST'])
@permission_classes([HasAPIKey])
def upvote_post(request,id):
    return upvote(request, 'post',id)

@csrf_exempt
@api_view(['POST'])
@permission_classes([HasAPIKey])
def upvote_comment(request,id):
    return upvote(request, 'comment',id)

"""@permission_classes([HasAPIKey])
@csrf_exempt"""
def upvote(request, item_str,id):
    key = request.META["HTTP_AUTHORIZATION"].split()[1]
    user = getUserFromKey(key)
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
                #item.user.karma += 1
                item.user.save()
                #item.votes += 1
                item.save()
            except IntegrityError:
                return JsonResponse({'success': False,'message':'Ya has votado'})

            return JsonResponse({'success': True,'message':'Votado con existo'})
        else: return JsonResponse({'success': False,'message':'No user'})


@csrf_exempt
@api_view(['POST'])
@permission_classes([HasAPIKey])
def unvote_post(request,id):
    return unvote(request, 'post',id)

@csrf_exempt
@api_view(['POST'])
@permission_classes([HasAPIKey])
def unvote_comment(request,id):
    return unvote(request, 'comment',id)


def unvote(request, item_str,id):
    key = request.META["HTTP_AUTHORIZATION"].split()[1]
    user = getUserFromKey(key)
    print(user.id)
    if request.method == 'POST':
        print(user.id)
        if user.id:
            hadVote = False
            if item_str == 'post':
                item = Post.objects.filter(id=id)[0]
                hadVote=PostVoteTracking.objects.filter(user=user, post=item).exists()
                print(hadVote)
                PostVoteTracking.objects.filter(user=user, post=item).delete()
            else:
                print("some")
                print(user.id)
                item = Comment.objects.filter(id=id)[0]
                hadVote=PostVoteTracking.objects.filter(user=user, comment=item).exists()
                CommentVoteTracking.objects.filter(user=user, comment=item).delete()
            print(hadVote)
            if (hadVote):
                #item.user.karma -= 1
                item.user.save()
                #item.votes -= 1
                item.save()
            else:
                print("Succes false")
                return JsonResponse({'success': False,'message':'No habias votado'})

            return JsonResponse({'success': True,'message':'Has desvotado'})
        else: return JsonResponse({'success': False,'messafe':'No user'})

class submission_vote(APIView):
    permission_classes = [HasAPIKey]
    http_method_names = ["POST"]

    def post(self, request, id, format=None):
        submission = Post.objects.get(id=id)
        user = getUserFromRequest(request)

        vote = PostVoteTracking.objects.filter(user=user).get(post=submission)
        
        if vote.count() > 1:
            return JsonResponse({'success' : False, 'message':'More than one vote selected'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if vote is None:
            newVote = PostVoteTracking.objects.create(user=user, post=submission)
            return JsonResponse({'upvote': True,'message':'Has votado la submission {id}'}, status=status.HTTP_202_ACCEPTED)
        
        deleted_vote = vote.delete()
        print(deleted_vote)
        return JsonResponse({'upvote': False,'message':'Has desvotado la submission {id}'}, status=status.HTTP_202_ACCEPTED)

class comment_vote(APIView):
    permission_classes = [HasAPIKey]
    http_method_names = ["POST"]

    def post(self, request, id, format=None):
        comment = Comment.objects.get(id=id)
        user = getUserFromRequest(request)

        vote = CommentVoteTracking.objects.filter(user=user).filter(comment=comment)

        if vote.count() > 1:
            return JsonResponse({'success' : False, 'message':'More than one vote selected'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if vote is None:
            newVote = CommentVoteTracking.objects.create(user=user, comment=comment)
            return JsonResponse({'upvote': True,'message':'Has votado el commentario {id}'}, status=status.HTTP_202_ACCEPTED)
        
        deleted_vote = vote.delete()
        print(deleted_vote)
        return JsonResponse({'upvote': False,'message':'Has desvotado el commentario {id}'}, status=status.HTTP_202_ACCEPTED)

class comment_detail(APIView):
    http_method_names = ["GET", "POST"]

    def get(self, request, id, format=None):
        comment = Comment.objects.get(id=id)
        fields = get_fields_from_request(request)

        serializer = CommentSerializer(comment, fields=fields)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id, format=None):
        user = getUserFromRequest(request)
        
        reply = Comment.objects.get(id=id)
        data = JSONParser().parse(request)

        serializer = CommentSerializer(data=data)
        if (serializer.is_valid()):
            post = None
            currentCom = reply

            while post is None:
                post = currentCom.post
                currentCom = currentCom.reply

            serializer.save(user=user)
            serializer.save(reply=reply)
            serializer.save(post=post)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## DEPRECADO - comment_detail
@csrf_exempt
@permission_classes([HasAPIKey])
def reply_comment(request, id):
    comment = Comment.objects.get(pk=id)
    if request.method == 'POST':
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        user = getUserFromKey(key)
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if (serializer.is_valid()):
            post = None
            currentCom = comment

            while post is None:
                post = currentCom.post
                currentCom = currentCom.reply

            serializer.save(user=user)
            serializer.save(reply=comment)
            serializer.save(post=post)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'GET':
        serializer = CommentSerializer(comment, many = False)
        return JsonResponse(serializer.data, status=201)