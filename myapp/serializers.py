
# serializers.py
from myapp.models import Author, Institution, Keyword, Reference, Article
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Utilisateur, Moderateur, Admin 
from . import models
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import ArticleDocument
import os
import requests
from PyPDF2 import PdfReader
from rest_framework import serializers
from django.conf import settings
from django.utils import timezone
import re
import json
import io
from django.core.serializers import serialize
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email']






class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = '__all__'

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Institution
        fields = '__all__'

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Keyword
        fields = '__all__'

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reference
        fields = '__all__'



class ArticleDocumentSerializer(DocumentSerializer):   
   class Meta:
        model=models.Article
        document=ArticleDocument
        fields = '__all__'
        def get_location(self ,obj):
          try:
             return obj.location.to_dict()
          except:
              return{}
       
class ArticleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Article
        authors = AuthorSerializer(many=True)
        institutions = InstitutionSerializer(many=True)
        keywords = KeywordSerializer(many=True)
        references =ReferenceSerializer(many=True)
        date_created=serializers.DateTimeField(read_only=True)
        fields = ['id','title', 'abstract', 'authors', 'institutions', 'keywords', 'pdf_url', 'references', 'date_created']



class UtilisateurSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    favoris = ArticleSerializer(many=True, required=False)

    class Meta:
        model = Utilisateur
        fields = ['id', 'user', 'first_name', 'family_name', 'favoris']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        favoris_data = validated_data.pop('favoris', [])
        user = User.objects.create_user(**user_data)

        # Create the Utilisateur instance
        utilisateur = Utilisateur.objects.create(user=user, **validated_data)

        # Set favoris for the Utilisateur instance (if needed)

        return utilisateur

    def update(self, instance, validated_data):
        # Exclude 'user' from validated_data to avoid unintentional username checks
        user_data = validated_data.pop('user', None)
        # Check if user_data is not None and username is not 'None'
        if user_data.get('username')=='None':
            pass
        else :
            instance.user.username = user_data.get('username', instance.user.username)
        instance.user.email = user_data.get('email', instance.user.email)
        instance.user.save()

        # Update Utilisateur fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.family_name = validated_data.get('family_name', instance.family_name)

        # Set favoris for the Utilisateur instance (if needed)

        # Save Utilisateur instance
        instance.save()

        return instance


class ModerateurSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Moderateur
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        favoris_data = validated_data.pop('favoris', [])

        # Create the User instance
        user = User.objects.create_user(**user_data)

        # Create the Moderateur instance
        moderateur = Moderateur.objects.create(user=user, **validated_data)

        # Set favoris for the Moderateur instance (if needed)

        return moderateur

    def update(self, instance, validated_data):
        # Exclude 'user' from validated_data to avoid unintentional username checks
        user_data = validated_data.pop('user', None)

        # Check if user_data is not None and username is not 'None'
        if user_data.get('username')=='None':
            pass
        else :
            instance.user.username = user_data.get('username', instance.user.username)
        instance.user.email = user_data.get('email', instance.user.email)
        instance.user.save()

        # Update Moderateur fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.family_name = validated_data.get('family_name', instance.family_name)

        # Save Moderateur instance
        instance.save()

        return instance


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        favoris_data = validated_data.pop('favoris', [])

        # Create the User instance
        user = User.objects.create_user(**user_data)

        # Create the Admin instance (assuming Admin extends Utilisateur)
        admin = Admin.objects.create(user=user, **validated_data)

        # Set favoris for the Admin instance (if needed)

        return admin

    def update(self, instance, validated_data):
        # Exclude 'user' from validated_data to avoid unintentional username checks
        user_data = validated_data.pop('user', None)

        # Check if user_data is not None and username is not 'None'
        if user_data.get('username')=='None':
            pass
        else :
            instance.user.username = user_data.get('username', instance.user.username)
        instance.user.email = user_data.get('email', instance.user.email)
        instance.user.save()

        # Update Admin fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.family_name = validated_data.get('family_name', instance.family_name)

        # Save Admin instance
        instance.save()

        return instance




class PDFTxtExtractionSerializer(serializers.Serializer):
    pdf_path = serializers.CharField()

    def extract_text_from_pdf(self, pdf_path):
        try:
            # Check if the input is a URL or a local file path
            if pdf_path.startswith(('http://', 'https://')):
                # If it's a URL, download the PDF
                response = requests.get(pdf_path)
                response.raise_for_status()
                pdf_content = response.content

            else:
                # If it's a local file path, read the PDF file
                if not os.path.exists(pdf_path):
                    raise serializers.ValidationError('Invalid local file path specified for the PDF.')

                with open(pdf_path, 'rb') as pdf_file:
                    pdf_content = pdf_file.read()

            # Extract text from the PDF content
            text = ''
            pdf_reader = PdfReader(io.BytesIO(pdf_content))
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            return text, pdf_path  


        except Exception as e:
            raise serializers.ValidationError(f"An error occurred: {str(e)}")

    def validate(self, data):
        pdf_path = data.get('pdf_path')

        if not pdf_path:
            raise serializers.ValidationError('Please provide a path to a PDF file or a URL.')

        # Call the text extraction function
        text, pdf_path = self.extract_text_from_pdf(pdf_path)

        # Save the text to a text file in the media directory of your Django project
        file_path = os.path.join(settings.MEDIA_ROOT, 'extracted_text.txt')

        with open(file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

        # Return both the relative path of the text file and the pdf_path in the media directory
        data['text_file'] = os.path.relpath(file_path, settings.MEDIA_ROOT)
        data['pdf_path'] = pdf_path  # Add the pdf_path to the returned data
        return data



from django.core.serializers import serialize
from django.forms.models import model_to_dict

class InfoExtractor(serializers.Serializer):
    content = serializers.CharField()

    def extract_info(self, pdf_path):
        # Assume pdf_path is passed to the extract_info method, but still, extract information from a text file
        file_path = self.validated_data['content']

        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
        except Exception as e:
            return {"error": str(e)}

        expressions_a_supprimer = [
        r'Interactive and Adaptable Media',
        r'Advances in Engineering Software 188 \(2024\) 103568',
        r'Advances in Engineering Software 188 \(2024\) 103571',
        r'Research paper',
        r'Contents lists available at ScienceDirect',
        r'Advances in Engineering Software',
        r'journal homepage: www.elsevier.com/locate/advengsoft',
        r'Research paper',
        r'2020 IEEE/ACM 42nd International Conference on Software Engineering Workshops \(ICSEW\)'
    ]

        for expression in expressions_a_supprimer:
         file_content = re.sub(expression, '', file_content, flags=re.MULTILINE)
          

        #Supprimer les sauts de ligne inutiles résultant de la suppression
        file_content = re.sub(r'\n{2,}', '\n', file_content)

        file_content= file_content.strip()
        references = []


        #Titre✅
        title_match = re.search(r'^([^\n]+)', file_content)
        title = title_match.group(1).strip() if title_match else None



        #Auteurs✅
        lines = file_content.split('\n')
        authors = []

    # Extract the first author(s) from the first line if it contains commas
        first_author_match = re.match(r'^\s*([^@]+)\s*$', lines[1])
        if first_author_match and ',' in lines[1]:
                 authors.extend([author.strip() for author in first_author_match.group(1).split(',')])
        else:
         authors.append(first_author_match.group(1))
        # Extract other authors based on specified conditions
         extracting_authors = False
         for i in range(2, len(lines)):
            line = lines[i]
            if 'Switzerland' in line or 'USA' in line:
                if '@' not in lines[i+1]:
                    new_author = lines[i+1].strip()
                    if new_author not in authors:
                        authors.append(new_author)  # Take the line after 'Switzerland' or 'USA' as an author
                    extracting_authors = True
            elif '@' in line:
                new_author = lines[i+1].strip()
                if new_author not in authors:
                    authors.append(new_author)  # Take the line after '@' as an author
                extracting_authors = True
            elif 'article info' in line.lower() or 'keywords' in line.lower() or 'abstract' in line.lower():
                break  # Stop if 'article info', 'keywords', or 'abstract' is found
            elif extracting_authors:
                new_author = line.strip()
                if new_author not in authors:
                    authors.append(new_author)
        #Institutions 
        lines = file_content.split('\n')
        institutions = []
         # Extract institutions between the title and the line containing '@'
        for i in range(1, len(lines)):
         line = lines[i]
         if '@' in line:
            break  # Stop if '@' is found
         else:
          institutions.append(line.strip())
        # Abstract✅
        abstract_match = re.search(r'(?i)\s*abstract[-]?\s*—?\s*(.*?)(?=\n\n|$)', file_content, re.DOTALL)
        abstract = abstract_match.group(1).strip() if abstract_match else None
        # Keywords✅
        keywords_match = re.search(r'(?i)\s*(?:KEYWORDS|index terms)\s*(.*?)(?:(?:I\.INTRODUCTION|introduction|1|acm|abstract)|(?=\n\n|$))', file_content, re.DOTALL)
        if keywords_match:
         keywords_str = keywords_match.group(1)
         if keywords_str is not None:
            keywords = re.split(r'[;,\n]', keywords_str)
            keywords = [kw.strip() for kw in keywords]
            keywords = list(filter(None, keywords))
        else: keywords=None
        # References✅
        references_match = re.search(r'(?i)\s*references\s*\n(.*?)(?=\n\n|$)', file_content, re.DOTALL)
        if references_match:
         references_str = references_match.group(1)
         if references_str is not None:
            references = [ref.strip() for ref in re.split(r'\n', references_str)]
            references = list(filter(None, references))
        return {
            'content': file_content,
            'title': title,
            'authors': authors,
            'institutions': institutions,
            'abstract': abstract,
            'keywords': keywords,
            'references': references,
            'pdf_path': pdf_path,  
        }
        
    def create_article(self, extracted_info):
        try:
            title = extracted_info['title']
            abstract = extracted_info['abstract']
            authors_data = extracted_info['authors']
            institutions_data = extracted_info['institutions']
            keywords_data = extracted_info['keywords']
            references_data = extracted_info['references']

            authors = [Author.objects.get_or_create(name=author)[0] for author in authors_data]
            institutions = [Institution.objects.get_or_create(name=institution)[0] for institution in institutions_data]
            keywords = [Keyword.objects.get_or_create(name=keyword)[0] for keyword in keywords_data] if keywords_data else []
            references = [Reference.objects.get_or_create(citation=citation)[0] for citation in references_data] if references_data else []

            article = Article.objects.create(
                title=title,
                abstract=abstract,
                text=extracted_info['content'],
                pdf_url=extracted_info['pdf_path'],
                treated=False,
                date_created=timezone.now(),
            )

            # Add the many-to-many relationships
            article.authors.set(authors)
            article.institutions.set(institutions)
            article.keywords.set(keywords)
            article.references.set(references)

            # Serialize the related data
            serialized_authors = [model_to_dict(author) for author in authors]
            serialized_institutions = [model_to_dict(institution) for institution in institutions]
            serialized_keywords = [model_to_dict(keyword) for keyword in keywords]
            serialized_references = [model_to_dict(reference) for reference in references]

            return {
                'article': {
                    'id': article.id,
                    'title': article.title,
                    'abstract': article.abstract,
                    'text': article.text,
                    'pdf_url': article.pdf_url,
                    'treated': article.treated,
                    'date_created': article.date_created,
                },
                'authors': serialized_authors,
                'institutions': serialized_institutions,
                'keywords': serialized_keywords,
                'references': serialized_references,
            }
        except Exception as e:
            print(f"Error during article creation: {e}")
            return None