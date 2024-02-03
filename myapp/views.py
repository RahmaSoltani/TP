# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from PyPDF2 import PdfReader
from django.http import JsonResponse
import requests
from  django_filters.rest_framework import DjangoFilterBackend
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
@api_view(['GET'])
def check_favorite_article(request, user_id, article_id):
    try:
        user = models.Utilisateur.objects.get(pk=user_id)
        article = Article.objects.get(pk=article_id)
        is_favorite = article in user.favoris.all()
        return Response({'is_favorite': is_favorite})
    except models.Utilisateur.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=404)

    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PATCH'])
def update_article(request, id):
    try:
        article = Article.objects.get(pk=id)
        data = request.data
        
        # Update the article fields if provided in the request data
        if 'title' in data:
            article.title = data['title']
        if 'abstract' in data:
            article.abstract = data['abstract']
        if 'text' in data:
            article.text = data['text']
        if 'treated' in data:
            article.treated = data['treated']
        if 'pdf_url' in data:
            article.pdf_url = data['pdf_url']
        
        # Update the many-to-many fields if provided in the request data
        if 'authors_names' in data:
            authors_names = data['authors_names'].split(',')
            authors = models.Author.objects.filter(name__in=authors_names)
            article.authors.set(authors)
        if 'institutions_names' in data:
            institutions_names = data['institutions_names'].split(',')
            institutions = models.Institution.objects.filter(name__in=institutions_names)
            article.institutions.set(institutions)
        if 'keywords_names' in data:
            keywords_names = data['keywords_names'].split(',')
            keywords = models.Keyword.objects.filter(name__in=keywords_names)
            article.keywords.set(keywords)
        if 'references_citations' in data:
            references_citations = data['references_citations'].split(',')
            references = models.Reference.objects.filter(citation__in=references_citations)
            article.references.set(references)
        
        # Save the updated article
        article.save()
        
        return Response({'message': 'Article updated successfully'}, status=status.HTTP_200_OK)
    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
class ArticleDocViewSet(DocumentViewSet):  
     document = ArticleDocument
     serializer_class = serializers.ArticleDocumentSerializer
     filter_backends = [
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
     ]
     search_fields = (
        '^title',
        '^abstract',
        '^authors.name',
        '^institutions.name',
        '^keywords.name',
        '^references,citation',


     )
     filter_backends = [DjangoFilterBackend]

     ordering_fields = {
        'date_created': 'date_created'
     }
     filter_fields = {
       'title',
        'abstract',
        'authors.name',
        'institutions.name',
        'keywords.name',
        'references,citation',    }
@api_view(['POST'])
def add_article_to_favorites(request):
    if request.method == 'POST':
        utilisateur_id = request.data.get('utilisateur_id')
        article_id = request.data.get('article_id')

        try:
            utilisateur = models.Utilisateur.objects.get(pk=utilisateur_id)
            article = models.Article.objects.get(pk=article_id)
        except models.Utilisateur.DoesNotExist:
            return Response({"error": "Utilisateur not found"}, status=404)
        except models.Article.DoesNotExist:
            return Response({"error": "Article not found"}, status=404)

        # Add the article to the favorites list
        utilisateur.favoris.add(article)
        
        # Return success response
        return Response({"message": "Article added to favorites successfully"}, status=200)
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

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from myapp.models import Article
from django.db.models import Q

@api_view(['GET'])
def article_details(request, id):
    try:
        article = Article.objects.get(pk=id)
        
        # Extract authors' names
        authors_names = ', '.join([author.name for author in article.authors.all()])
        
        # Extract institutions' names
        institutions_names = ', '.join([institution.name for institution in article.institutions.all()])
        
        # Extract references' citations
        references_citations = ', '.join([reference.citation for reference in article.references.all()])
        
        # Extract keywords' names
        keywords_names = ', '.join([keyword.name for keyword in article.keywords.all()])
        
        # Add other attributes here
        
        response_data = {
            'title': article.title,
            'abstract': article.abstract,
            'authors_names': authors_names,
            'institutions_names': institutions_names,
            'references_citations': references_citations,
            'keywords_names': keywords_names,
            'text':article.text,
            # Add other attributes as needed
        }
        
        return Response(response_data)
    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def login(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

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

def search_and_filter_articles(request):
    word = request.data.get('word', '')
    filter_field = request.data.get('filter_field', None)

    articles = Article.objects.all()

    if word:
        # Filter articles based on the given word in multiple fields
        if filter_field:
            # Filter based on the specified field if provided
            if filter_field == 'keywords':
                articles = articles.filter(keywords__name__icontains=word)
            elif filter_field == 'institutions':
                articles = articles.filter(institutions__name__icontains=word)
            elif filter_field == 'authors':
                articles = articles.filter(authors__name__icontains=word)
            else:
                # Invalid filter field provided, fallback to searching in all fields
                articles = articles.filter(
                    Q(title__icontains=word) |
                    Q(abstract__icontains=word) |
                    Q(keywords__name__icontains=word) |
                    Q(institutions__name__icontains=word) |
                    Q(authors__name__icontains=word)
                )
        else:
            # Filter based on the given word in all searchable fields
            articles = articles.filter(
                Q(title__icontains=word) |
                Q(abstract__icontains=word) |
                Q(keywords__name__icontains=word) |
                Q(institutions__name__icontains=word) |
                Q(authors__name__icontains=word)
            )

    # Serialize the filtered articles
    serializer = serializers.ArticleSerializer(articles, many=True)
    return Response(serializer.data)

    # Return the serialized data as a JSON response
    return Response(serializer.data)


from django.http import JsonResponse
from .models import Article
from .serializers import ArticleSerializer
@api_view(['GET'])

def non_treated_articles(request):
    try:
        # Get non-treated articles using the custom manager
        non_treated_articles = Article.objects.filter(treated=False)

        # Serialize the non-treated articles
        serializer = ArticleSerializer(non_treated_articles, many=True)
        
        # Return the serialized non-treated articles as JSON response
        return Response(serializer.data)
    except Article.DoesNotExist:
        return Response({'error': 'No non-treated articles found'}, status=404)
from django.http import JsonResponse
from .models import Article
from .serializers import ArticleSerializer
@api_view(['GET'])

def get_article(request, article_id):
    try:
        # Retrieve the article by its ID
        article = Article.objects.get(pk=article_id)
        
        # Serialize the article
        serializer = ArticleSerializer(article)
        
        # Return the serialized article as JSON response
        return Response(serializer.data)
    except Article.DoesNotExist:
        # Return a 404 response if the article does not exist
        return Response({'error': 'Article not found'}, status=404)
@api_view(['GET'])

def list_favorite_articles(request, utilisateur_id):
    try:
        utilisateur = models.Utilisateur.objects.get(pk=utilisateur_id)
        favoris_articles = utilisateur.favoris.all()
        serializer = serializers.ArticleSerializer(favoris_articles, many=True)
        return Response(serializer.data)
    except models.Utilisateur.DoesNotExist:
        return Response({'error': 'Utilisateur not found'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['POST'])
def treat_article(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        article.treated = True
        article.save()
        return JsonResponse({'message': 'Article treated successfully'}, status=200)
    except Article.DoesNotExist:
        return JsonResponse({'error': 'Article not found'}, status=404)
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

    
class ExtractionView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract common data from the request
        pdf_path = request.data.get('pdf_path', '')

        # Text extraction
        text_serializer = PDFTxtExtractionSerializer(data=request.data)
        if text_serializer.is_valid():
            text_data = {'text_file': text_serializer.validated_data['text_file']}
        else:
            return Response(text_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Information extraction
        info_serializer = InfoExtractor(data=request.data)
        if info_serializer.is_valid():
            info_data = info_serializer.extract_info(pdf_path)
            # Create article using the extracted information
            article = info_serializer.create_article(info_data)
            if article:
                print(f"Article created successfully: {article}")
            else:
                print("Article creation failed.")
        else:
            return Response(info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Combine the results
        combined_data = {**text_data, **info_data}

        return Response(combined_data, status=status.HTTP_200_OK)