# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from PyPDF2 import PdfReader
from django.http import JsonResponse
import requests
import PyPDF2
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
class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.UtilisateurSerializer

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
import requests
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileReader
import requests
"""
@api_view(['POST', 'GET'])
def extract_text_from_pdf_url(request):
    url= request.data.get('url')
    if not url :

    if request.method == 'GET':
        return Response({'error': 'GET method not supported. Use POST with a JSON body containing the PDF URL.'}, status=400)

    pdf_url = request.data.get('pdf_url')
    print(request.data)
    if not pdf_url:
        return Response({'error': 'PDF URL is required'}, status=400)

    try:
        # Download the PDF content
        response = requests.get(pdf_url)
        response.raise_for_status()

        # Write the PDF content to a temporary file
        with open('temp.pdf', 'wb') as pdf_file:
            pdf_file.write(response.content)

        # Read the PDF and extract text
        with open('temp.pdf', 'rb') as pdf_file:
            pdf_reader = PdfFileReader(pdf_file)
            pdf_text = ''
            for page_num in range(pdf_reader.numPages):
                pdf_text += pdf_reader.getPage(page_num).extractText()

        return Response({'pdf_text': pdf_text}, status=200)

    except Exception as e:
        return Response({'error': f'Error extracting text from PDF: {str(e)}'}, status=500)
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from PyPDF2 import PdfFileReader
import requests

@api_view(['POST'])
def extract_first_word_from_pdf_url(request):
    try:
        pdf_url = request.data.get('pdf_url')

        if not pdf_url:
            return Response({'error': 'PDF URL is required'}, status=400)

        # Check if the URL ends with '.pdf' to ensure it's a PDF file
        if not pdf_url.lower().endswith('.pdf'):
            return Response({'error': 'The provided URL is not a PDF'}, status=400)

        # Download the PDF content
        response = requests.get(pdf_url)
        response.raise_for_status()

        # Write the PDF content to a temporary file
        with open('temp.pdf', 'wb') as pdf_file:
            pdf_file.write(response.content)

        # Read the PDF and extract text
        pdf_text = extract_text_from_pdf('temp.pdf')

        # Extract the first word
        first_word = pdf_text.split()[0] if pdf_text else ''

        return Response({'first_word': first_word}, status=200)

    except requests.exceptions.RequestException as e:
        return Response({'error': f'Error making HTTP request: {str(e)}'}, status=500)

    except Exception as e:
        return Response({'error': f'Error extracting text from PDF: {str(e)}'}, status=500)

def extract_text_from_pdf(pdf_file_path):
    try:
        # Read the PDF and extract text
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_reader = PdfFileReader(pdf_file)
            pdf_text = ''
            for page_num in range(pdf_reader.numPages):
                pdf_text += pdf_reader.getPage(page_num).extractText()

        return pdf_text

    except Exception as e:
        raise ValueError(f'Error extracting text from PDF: {str(e)}')

from drf_pdf.response import PDFResponse
from drf_pdf.renderer import PDFRenderer

#from my_pdf_package import get_pdf
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
"""
class PDFHandler(APIView):

    renderer_classes = (PDFRenderer, JSONRenderer)

    def get(self, request, pdf_id):
        pdf = get_pdf(pdf_id)
        if not pdf:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        return PDFResponse(
            pdf=pdf,
            file_name=pdf_id,
            status=status.HTTP_200_OK
        )
"""