from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import exceptions , status
from accounts.models import HNUser
from homepage.models import *
from .serializers import *
from django.db.utils import IntegrityError
from .permissions import *


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
        raise exceptions.NotFound("User with ID: %i was not found" % id,)
     
def getUserFromRequest(request) -> HNUser:
    print("Getting user from request")
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        return HNUser.objects.get(key=key)
    except KeyError: 
        raise exceptions.NotAuthenticated(detail="Api-Key credentials were not provided.")
    except HNUser.DoesNotExist:
        raise exceptions.NotFound(detail="Api-Key has no user associated", code=status.HTTP_410_GONE)

class user_list(APIView):
    # No permission needed
    permission_classes = []
    http_method_names = ['get', 'post']

    def get(self, request, format=None):
        fields = get_fields_from_request(request)

        users = HNUser.objects.all()
        users = filter_by_id_from_request(request=request, query_set=users)
        
        serializer = HNUserSerializer(users, fields=fields, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def post(self, request, fomat=None):
        data = JSONParser().parse(request)
        input = HNUserSerializer(data=data)

        if input.is_valid():
            try:
                newUser = input.save()
                fields = ('id','username', 'email')
                serializer = HNUserSerializer(newUser, fields=fields)
                output:dict = serializer.data
                output['key'] = newUser.key
                return JsonResponse(output, status = status.HTTP_201_CREATED)
            except IntegrityError as e:
                print(e)
                return JsonResponse({'email':[ "Email already in use." ]}, status= status.HTTP_409_CONFLICT)
        return JsonResponse(input.errors,status=status.HTTP_400_BAD_REQUEST)

class user_detail(APIView):
    permission_classes = [ApiKeyUserOrReadOnly]
    http_method_names = ['get', 'put', 'delete']

    def get(self, request, id, format=None):
        user = getUserFromID(id)
        fields = get_fields_from_request(request)

        serializer = HNUserSerializer(user, fields=fields)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        user = getUserFromID(id)
        key_user = getUserFromRequest(request)

        if user != key_user: raise exceptions.PermissionDenied("Cannot update other user's info")

        data = JSONParser().parse(request)
        serializer = UpdateUserSerializer(user, data=data)
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        user = getUserFromID(id)
        requestUser = getUserFromRequest(request)
        
        if user != requestUser and not requestUser.is_admin:
            raise exceptions.PermissionDenied("Cannot delete other users")
        user.delete()
        return JsonResponse({"detail":"User has been deleted"}, status= status.HTTP_202_ACCEPTED)

class user_comments(APIView):
    permission_classes = []
    http_method_names = ['get']

    def user_comments(self, user):
        user_comments = Comment.objects.filter(user=user)
        serializer = CommentSerializer(user_comments, many=True)
        return JsonResponse(serializer.data, safe=False)

    def upvoted_comments(self, user):
        upvoted_comments = Comment.objects.filter(upvotes__user=user)
        serializer = CommentSerializer(upvoted_comments, many=True)
        return  JsonResponse(serializer.data, safe=False)

    def get(self, request, id, format=None):
        user = getUserFromID(id)

        upvoted = string_to_bool(request.GET.get('upvoted', 'False'))

        if upvoted:
            if user != getUserFromRequest(request): 
                raise exceptions.PermissionDenied("Cannot view other user's upvoted comments")
            return self.upvoted_comments(user)
        else:
            return self.user_comments(user)

class user_submissions(APIView):
    permission_classes = []
    http_method_names = ['get']

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

        upvoted = string_to_bool(request.GET.get('upvoted', 'False'))

        if upvoted:
            if user != getUserFromRequest(request):
                raise exceptions.PermissionDenied("Cannot view other user's upvoted submissions")
            return self.upvoted_submission(user)
        else:
            return self.user_submissions(user)


    #  SUBMISSION  #

def getSubmissionFromID(id) -> Post:
    try:
        return Post.objects.get(id=id)
    except:
        raise exceptions.NotFound("Submission with ID: %i was not found" % id)

def order_query_set(query_set, field:str, ascending=False):
    if field is None: return query_set
    if field == 'numComments': field = 'num_comments'
    if field == 'votes': field = 'num_votes' # 'upvotes'
    if not ascending: field= '-'+ field
    try:
        return query_set.order_by(field)
    except Exception as e:
        print(type(e), e)
        print("ERROR oredering by field:",field)
    return query_set

class submission_list(APIView):
    permission_classes = [ApiKeyUserOrReadOnly]
    http_method_names = ['get','post']

    def get(self, request, format=None):
        fields = get_fields_from_request(request)
        order_by = request.GET.get('order_by',None)
        ascending = string_to_bool(request.GET.get('ascending', 'false'))
        type = request.GET.get('type','all').lower()

        submissions = order_query_set(Post.objects.all(), order_by, ascending)
        submissions = filter_by_id_from_request(request, submissions)
        
        if (type == 'ask'):
            submissions = submissions.filter(url=None)
        elif(type == 'url'):
            submissions = submissions.filter(text=None)
        

        serializer = PostSerializer(submissions, fields=fields, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        user = getUserFromRequest(request)

        data = JSONParser().parse(request)

        serializer = PostSerializer(data=data)
        if (serializer.is_valid()):
            try:
                serializer.save(userID=user.id)
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return JsonResponse({"url":["URL must be unique"]}, status=status.HTTP_409_CONFLICT)
        return JsonResponse(serializer.errors, status=400)

class submission_detail(APIView):
    permission_classes = [ApiKeyUserOrReadOnly]
    http_method_names = ['get', 'delete']

    def get(self, request, id, format=None):
        fields = get_fields_from_request(request)
        submission = getSubmissionFromID(id)
        serializer = PostSerializer(submission, fields=fields)
        return JsonResponse(serializer.data, status = status.HTTP_200_OK)

    def delete(self, request, id, format=None):
        requestUser = getUserFromRequest(request)
        submission = getSubmissionFromID(id)

        if (submission.user != requestUser and not requestUser.is_admin):
            raise exceptions.PermissionDenied("Cannot delete other user's post")
        submission.delete()
        return JsonResponse({'detail': 'Post has been deleted'}, status= status.HTTP_202_ACCEPTED)

class submission_comments(APIView):
    permission_classes = [ApiKeyUserOrReadOnly]
    http_method_names = ['get', 'post']
    
    def get(self, request, id, format=None):
        submission = getSubmissionFromID(id)
        comment_list = submission.comment_set
        serializer = CommentSerializer(comment_list, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, id, format=None):
        user = getUserFromRequest(request)
        submission = getSubmissionFromID(id)

        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)

        if (serializer.is_valid()):
            serializer.save(userID=user.id,postID=submission.id)
            #serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
           
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #    VOTE     #

class submission_vote(APIView):
    permission_classes = [HasAPIKey]
    http_method_names = ['get','put','post','delete']

    def canVote(self, user:HNUser, submission:Post) -> tuple [bool, str, int]:
        if (submission.user == user): return False, 'Cannot vote own submission',status.HTTP_403_FORBIDDEN
        vote = PostVoteTracking.objects.filter(user=user).filter(post=submission)
        if (vote.count() == 0): return True, ('User %s no ha votado la submission %i' % (user.username, submission.id)), status.HTTP_202_ACCEPTED
        if (vote.count() == 1): return False, ('User %s ya ha votado la submission %i' % (user.username, submission.id)), status.HTTP_202_ACCEPTED
        return False, 'More than one vote selected', status.HTTP_500_INTERNAL_SERVER_ERROR

    def vote(self, user:HNUser, submission:Post):
        canVote, message, code = self.canVote(user,submission)
        if (not canVote): raise exceptions.APIException(detail=message, code=code)
        return PostVoteTracking.objects.create(user=user, post=submission)
        
    def unvote(self, user:HNUser, submission:Post):
        canVote, message, code = self.canVote(user,submission)
        #if (not canVote): raise exceptions.APIException(detail=message, code=code)
        deleted_vote = PostVoteTracking.objects.filter(user=user).filter(post=submission).delete()
        print(deleted_vote)
        return deleted_vote
  

    def get(self, request, id, format=None):
        submission = getSubmissionFromID(id)
        user = getUserFromRequest(request)
        canVote, message, code = self.canVote(user,submission)
        
        return JsonResponse({'can_vote' : canVote, 'message' : message}, status=code)

    def put(self, request, id, format=None):
        submission = getSubmissionFromID(id)
        user = getUserFromRequest(request)

        canVote, message, code = self.canVote(user, submission)

        if (code == status.HTTP_202_ACCEPTED):
            if (canVote):
                self.vote(user, submission)
                return JsonResponse({'success' : True, 'upvote': True, 'message':'Has votado la submission %i' % id}, status=status.HTTP_202_ACCEPTED)
            else:
                self.unvote(user,submission)
                return JsonResponse({'success' : True, 'upvote': False,'message':'Has desvotado la submission %i' % id}, status=status.HTTP_202_ACCEPTED)
        return JsonResponse({'success' : False, 'message' : message}, status = code)
            
    def post(self, request, id, format=None):
        submission = getSubmissionFromID(id)
        user = getUserFromRequest(request)

        canVote, message, code = self.canVote(user, submission)

        if (canVote):
            self.vote(user,submission)
            return JsonResponse({'success' : True, 'upvote': True, 'message':'Has votado la submission %i' % id}, status=status.HTTP_202_ACCEPTED)
        return JsonResponse({'success' : canVote, 'upvote': False, 'message':message}, status = code)        

    def delete(self, request, id, format=None):
        submission = getSubmissionFromID(id)
        user = getUserFromRequest(request)

        canVote, message, code = self.canVote(user, submission)
        try:
            self.unvote(user, submission)
            return JsonResponse({'success' : True, 'upvote': False,'message':'Has desvotado la submission %i' % id}, status=status.HTTP_202_ACCEPTED)
        except:
            return JsonResponse({'success' : canVote, 'upvote': False, 'message':message}, status = code)        


class comment_vote(APIView):
    permission_classes = [HasAPIKey]
    http_method_names = ['get','put','post','delete']
    
    def canVote(self, user:HNUser, comment:Comment) -> tuple [bool, str, int]:
        if (comment.user == user): return False, 'Cannot vote your own comments',status.HTTP_403_FORBIDDEN
        vote = CommentVoteTracking.objects.filter(user=user).filter(comment=comment)
        if (vote.count() == 0): return True, ('User %s no ha votado el comment %i' % (user.username, comment.id)), status.HTTP_202_ACCEPTED
        if (vote.count() == 1): return False, ('User %s ya ha votado el comment %i' % (user.username, comment.id)), status.HTTP_202_ACCEPTED
        return False, 'More than one vote selected', status.HTTP_500_INTERNAL_SERVER_ERROR

    def vote(self, user:HNUser, comment:Comment):
        canVote, message, code = self.canVote(user,comment)
        if (not canVote): raise exceptions.APIException(detail=message, code=code)
        return CommentVoteTracking.objects.create(user=user, comment=comment)
        
    def unvote(self, user:HNUser, comment:Comment):
        canVote, message, code = self.canVote(user,comment)
        #if (not canVote): raise exceptions.APIException(detail=message, code=code)
        deleted_vote = CommentVoteTracking.objects.filter(user=user).filter(comment=comment).delete()
        print(deleted_vote)
        return deleted_vote
  

    def get(self, request, id, format=None):
        comment = getCommentFromID(id=id)
        user = getUserFromRequest(request)
        canVote, message, code = self.canVote(user,comment)
        
        return JsonResponse({'can_vote' : canVote, 'message' : message}, status=code)

    def put(self, request, id, format=None):
        comment = getCommentFromID(id=id)
        user = getUserFromRequest(request)

        canVote, message, code = self.canVote(user, comment)

        if (code == status.HTTP_202_ACCEPTED):
            if (canVote):
                self.vote(user, comment)
                return JsonResponse({'success' : True, 'upvote': True, 'message':'Has votado el comentario %i' % id}, status=status.HTTP_202_ACCEPTED)
            else:
                self.unvote(user,comment)
                return JsonResponse({'success' : True, 'upvote': False,'message':'Has desvotado el comentario %i' % id}, status=status.HTTP_202_ACCEPTED)
        return JsonResponse({'success' : False, 'message' : message}, status = code)
            
    def post(self, request, id, format=None):
        comment = getCommentFromID(id=id)
        user = getUserFromRequest(request)

        canVote, message, code = self.canVote(user, comment)

        if (canVote):
            self.vote(user,comment)
            return JsonResponse({'success' : True, 'upvote': True, 'message':'Has votado el comentario %i' % id}, status=status.HTTP_202_ACCEPTED)
        return JsonResponse({'success' : canVote, 'upvote': False, 'message':message}, status = code)        

    def delete(self, request, id, format=None):
        comment = getCommentFromID(id=id)
        user = getUserFromRequest(request)

        canVote, message, code = self.canVote(user, comment)
        try:
            self.unvote(user, comment)
            return JsonResponse({'success' : True, 'upvote': False,'message':'Has desvotado el comentario %i' % id}, status=status.HTTP_202_ACCEPTED)
        except:
            return JsonResponse({'success' : canVote, 'upvote': False, 'message':message}, status = code)        

"""
    def post(self, request, id, format=None):
        comment = getCommentFromID(id=id)
        user = getUserFromRequest(request)

        if (comment.user == user): return JsonResponse({'success' : False, 'message':'Cannot vote own comment'}, status=status.HTTP_403_FORBIDDEN)


        vote = CommentVoteTracking.objects.filter(user=user).filter(comment=comment)
        if vote.count() > 1:
            return JsonResponse({'success' : False, 'message':'More than one vote selected'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if vote.count() == 0:
            newVote = CommentVoteTracking.objects.create(user=user, comment=comment)
            return JsonResponse({'succes' : True, 'upvote': True,'message':'Has votado el commentario %i' % id}, status=status.HTTP_202_ACCEPTED)
        
        deleted_vote = vote.delete()
        print(deleted_vote)
        return JsonResponse({'succes' : True, 'upvote': False,'message':'Has desvotado el commentario %i' % id}, status=status.HTTP_202_ACCEPTED)
"""

    #   COMMENT    #

def getCommentFromID(id) -> Comment:
    try:
        return Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        raise exceptions.NotFound("Comment with ID: %i was not found." % id)

def getPostFromComment(reply:Comment) -> Post:
    if reply.post is not None: return reply.post
    if (reply.reply is None): raise exceptions.ValidationError(detail='Comment is not attached to post', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return getPostFromComment(reply.reply)

class comment_detail(APIView):
    permission_classes = [ApiKeyUserOrReadOnly]
    http_method_names = ['get', 'post']

    def get(self, request, id, format=None):
        comment = getCommentFromID(id)
        fields = get_fields_from_request(request)

        serializer = CommentSerializer(comment, fields=fields)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id, format=None):
        user = getUserFromRequest(request)
        reply = getCommentFromID(id)
        post = getPostFromComment(reply)

        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)

        if (serializer.is_valid()):
            
            serializer.save(userID=user.id, postID=post.id, replyID=reply.id)

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        requestUser = getUserFromRequest(request)
        comment = getCommentFromID(id=id)

        if comment.user != requestUser and not requestUser.is_admin:
            raise exceptions.PermissionDenied("Cannot delete other user's comment")

        comment.delete()
        return JsonResponse({'detail': 'Comment has been deleted'}, status= status.HTTP_202_ACCEPTED)
