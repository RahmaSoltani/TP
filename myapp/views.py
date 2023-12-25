# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PDFTxtExtractionSerializer
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    OrderingFilterBackend,
)
from rest_framework_simplejwt.tokens import RefreshToken

from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from .documents import ArticleDocument
from rest_framework import viewsets
from . import models
from . import serializers , documents
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.pagination import LimitOffsetPagination

from rest_framework.response import Response
from rest_framework import status
#from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
"""    
class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = models.Utilisateur.objects.all()
    serializer_class = serializers.UtilisateurSerializer
"""
class ModerateurViewSet(viewsets.ModelViewSet):
    queryset = models.Moderateur.objects.all()
    serializer_class = serializers.ModerateurSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = models.Admin.objects.all()
    serializer_class = serializers.AdminSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset=models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer

class RefrenceViewSet(viewsets.ModelViewSet):
    queryset=models.Institution.objects.all()
    serializer_class = serializers.ReferenceSerializer

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = models.Keyword.objects.all()
    serializer_class = serializers.KeywordSerializer

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = models.Institution.objects.all()
    serializer_class = serializers.InstitutionSerializer

class RefrenceViewSet(viewsets.ModelViewSet):
    queryset = models.Reference.objects.all()
    serializer_class = serializers.ReferenceSerializer

class ArticleDocViewSet(DocumentViewSet):  
     document = ArticleDocument
     serializer_class = serializers.ArticleDocumentSerializer
     filter_backends = [
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
     ]
     search_fields = (
        'title',
        'abstract',
        'authors.name',
        'institutions.name',
        'keywords.name',
        'references,citation',


     )
     ordering_fields = {
        'date_created': 'date_created'
     }
     filter_fields = {
       'title',
       'abstract',    }


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    # Authenticate user with old password
    if not authenticate(username=user.username, password=old_password):
        return Response({'detail': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

    # Change the password
    user.password = make_password(new_password)
    user.save()

    return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])

def login(request):
    username=request.data.get('username')
    password=request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        user_type = None

        try:
            moderateur = user.moderateur_set.get()
            user_type = 'moderateur'
        except models.Moderateur.DoesNotExist:
            pass

        if user_type is None:
            try:
                utilisateur = user.utilisateur_set.get()
                user_type = 'utilisateur'
            except models.Utilisateur.DoesNotExist:
                pass

        if user_type is None:
            try:
                admin = user.admin_set.get()
                user_type = 'admin'
            except models.Admin.DoesNotExist:
                pass
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({'access_token': access_token,'user_type':user_type}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": f"Error during logout: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExtractTextFromPDFView(APIView):
    def post(self, request, format=None):
        serializer = PDFTxtExtractionSerializer(data=request.data)

        if serializer.is_valid():
            return Response({'text_file': serializer.validated_data['text_file']}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
