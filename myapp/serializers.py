
# serializers.py

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
import re
import json

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']






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
        if user_data and user_data.get('username') is not None:
            instance.user.username = user_data.get('username', instance.user.username)
        instance.user.email = user_data.get('email', instance.user.email)
        instance.user.save()

        # Update Admin fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.family_name = validated_data.get('family_name', instance.family_name)

        # Save Admin instance
        instance.save()

        return instance

class ArticleDocumentSerializer(DocumentSerializer):   
   class Meta:
        document=ArticleDocument
        fields = '__all__'
   
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

        # Create the User instance
        user = User.objects.create_user(**user_data)

        # Create the Utilisateur instance
        utilisateur = Utilisateur.objects.create(user=user, **validated_data)

        # Set favoris for the Utilisateur instance (if needed)

        return utilisateur

    def update(self, instance, validated_data):
        # Exclude 'user' from validated_data to avoid unintentional username checks
        user_data = validated_data.pop('user', None)

        # Check if user_data is not None and username is not 'None'
        if user_data and user_data.get('username') is not None:
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
        if user_data and user_data.get('username') is not None:
            instance.user.username = user_data.get('username', instance.user.username)
        instance.user.email = user_data.get('email', instance.user.email)
        instance.user.save()

        # Update Moderateur fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.family_name = validated_data.get('family_name', instance.family_name)

        # Save Moderateur instance
        instance.save()

        return instance





class PDFTxtExtractionSerializer(serializers.Serializer):
    pdf_path = serializers.CharField()

    def extract_text_from_pdf(self, pdf_path):
         try:
            # Vérifiez si le fichier PDF existe
            if not os.path.exists(pdf_path):
                raise serializers.ValidationError('Le chemin du fichier PDF spécifié est invalide.')

            # Extraire le texte du PDF
            text = ''
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()

            return text

         except Exception as e:
            raise serializers.ValidationError(f"Une erreur s'est produite : {str(e)}")
        
    def validate(self, data):
        pdf_path = data.get('pdf_path')

        if not pdf_path:
            raise serializers.ValidationError('Veuillez fournir un chemin vers un fichier PDF')

        # Appeler la fonction d'extraction de texte
        text = self.extract_text_from_pdf(pdf_path)

        # Enregistrez le texte dans un fichier texte dans le répertoire media de votre projet Django
        file_path = os.path.join(settings.MEDIA_ROOT, 'texte_extrait.txt')

        with open(file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

        # Retournez le chemin relatif du fichier texte dans le répertoire media
        data['text_file'] = os.path.relpath(file_path, settings.MEDIA_ROOT)
        return data
