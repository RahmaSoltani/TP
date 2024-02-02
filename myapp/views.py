# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from PyPDF2 import PdfReader
from django.http import JsonResponse
import requests
import PyPDF2
from rest_framework import status
from .serializers import PDFTxtExtractionSerializer
from .serializers import InfoExtractor
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
    queryset = models.Utilisateur.objects.all()
    serializer_class = serializers.UtilisateurSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset=models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer

class RefrenceViewSet(viewsets.ModelViewSet):
    queryset=models.Institution.objects.using('article').all()
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
    
    id = request.data.get('id')
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    user=models.User.objects.get(id=id)

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
            id=moderateur.id
        except models.Moderateur.DoesNotExist:
            pass

        if user_type is None:
            try:
                utilisateur = user.utilisateur_set.get()
                user_type = 'utilisateur'
                id=utilisateur.id
            except models.Utilisateur.DoesNotExist:
                pass

        if user_type is None:
            try:
                admin = user.admin_set.get()
                user_type = 'admin'
                id=admin.id
            except models.Admin.DoesNotExist:
                pass
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({'access_token': access_token,'user_type':user_type,'id':id,'username':username}, status=status.HTTP_200_OK)
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


"""
import requests
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileReader
import requests

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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import fitz  # PyMuPDF

@api_view(['GET', 'POST'])
@csrf_exempt
def extract_text_from_pdf_view(request):
    if request.method == 'POST':
        pdf_url = request.data.get('pdf_url')  # Get the PDF URL from the POST data

        try:
            if pdf_url.startswith(('http://', 'https://')):
                # Fetch the PDF file from the URL
                response = requests.get(pdf_url)
                response.raise_for_status()

                # Open the PDF using PyMuPDF
                pdf_document = fitz.open("pdf", response.content)

            else:
                # Open the local PDF file
                with open(pdf_url, 'rb') as local_pdf:
                    pdf_document = fitz.open("pdf", local_pdf.read())

            # Extract text from each page
            text_content = ""
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text_content += page.get_text()

            # Close the PDF document
            pdf_document.close()

            return Response({'pdf_text': text_content})

        except Exception as e:
            return Response({'error': f"Error: {str(e)}"}, status=500)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

import fitz
import re
@api_view(['POST'])
@csrf_exempt
def extract_specific_sections_from_pdf(request):
    if request.method == 'POST':
        pdf_url = request.data.get('pdf_url')

        try:
            if pdf_url.startswith(('http://', 'https://')):
                # Fetch the PDF file from the URL
                response = requests.get(pdf_url)
                response.raise_for_status()
                pdf_content = response.content
            else:
                # Open the local PDF file
                with open(pdf_url, 'rb') as local_pdf:
                    pdf_content = local_pdf.read()

            # Open the PDF using PyMuPDF
            pdf_document = fitz.open("pdf", pdf_content)

            # Extract the abstract
            abstract = ""
            in_abstract = False
            end_pattern = re.compile(r'\b(?:categories and subject descriptors|index terms|motivation and significance|ccs concepts|use cases|keywords|introduction)\b', re.IGNORECASE)

            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                blocks = page.get_text("blocks", clip=page.rect)

                for block in blocks:
                    text = block[4]  # The text content is at index 4

                    # Check if the current text indicates the start of the abstract
                    if re.search(r'\babstract\b|\bA B S T R A C T\b|\bABSTRACT\b', text, re.IGNORECASE):
                        in_abstract = True

                    # Check if the current text indicates the end of the abstract
                    if in_abstract and end_pattern.search(text):
                        abstract += text + ' '
                        abstract = abstract.replace('\n', ' ').strip()
                        abstract.save()
                        return Response({'abstract': abstract})

                    # Add text to the abstract if in the abstract section
                    if in_abstract:
                        abstract += text + ' '

            # Remove unwanted characters within the abstract
            abstract = abstract.replace('\n', ' ').strip()

            # Close the PDF document
            pdf_document.close()

            return Response({'abstract': abstract})

        except Exception as e:
            return Response({'error': f"Error: {str(e)}"}, status=500)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@api_view(['POST'])
def check_username(request):
    if request.method == 'POST':
        username = request.data.get('username')

        if User.objects.filter(username=username).exists():
            return Response({'is_taken': True})
        else:
            return Response({'is_taken': False})

    return Response({'error': 'Invalid request method'})
@api_view(['POST'])
def check_email(request):
    if request.method == 'POST':
        email = request.data.get('email')

        if User.objects.filter(email=email).exists():
            return Response({'is_taken': True})
        else:
            return Response({'is_taken': False})

    return Response({'error': 'Invalid request method'})
from django.core.mail import send_mail
import random

@api_view(['POST'])
def send_email(request):
 if request.method == 'POST':
    email = request.data.get('email')
    code= str(random.randint(100000, 999999))
    subject = 'Confirmation Code'
    message = f'Your confirmation code is: {code}'
    from_email = 'baraaassociation595@gmail.com'  # Replace with your email
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
    return Response({'code':code})

class ExtractInfoFromTextView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = InfoExtractor(data=request.data)

        if serializer.is_valid():
            extracted_info = serializer.extract_info()
            return Response(extracted_info, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)