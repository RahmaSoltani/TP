
# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Utilisateur, Moderateur, Admin 
from . import models
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import ArticleDocument
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']





class ModerateurSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Moderateur
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        moderateur = Moderateur.objects.create(user=user, **validated_data)
        return moderateur

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        # Update user fields if provided
        if user_data.username== user.username:
            pass
        else : 
           if User.objects.filter(username=user_data.username).exists :
                raise serializers.ValidationError("The new username already exists.")
           else :
               user.username=user_data.username
        if user_data.email== user.email:
            pass
        else : 
           if User.objects.filter(email=user_data.email).exists :
                raise serializers.ValidationError("The new email already exists.")
           else :
               user.email=user_data.email               
               
       
        instance.user=user
        instance.user.save()

        # Update Moderateur fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.family_name = validated_data.get('family_name', instance.family_name)
        instance.save()

        return instance

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
        user = User.objects.create_user(**user_data)
        admin = Admin.objects.create(user=user, **validated_data)
        return admin

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.save()

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.family_name = validated_data.get('family_name', instance.family_name)
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
        fields = ['id','title', 'abstract', 'authors', 'institutions', 'keywords', 'pdf_url', 'references', 'date_created']

"""
class UtilisateurSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Utilisateur
#       favoris=ArticleSerializer(many=True)
        fields = ['id', 'user', 'first_name', 'family_name']
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        favoris_data = validated_data.pop('favoris', [])

        # Create the User instance
        user = User.objects.create_user(**user_data)

        # Create the Utilisateur instance
        utilisateur = Utilisateur.objects.create(user=user, **validated_data)

        # Set favoris for the Utilisateur instance

        return utilisateur

    def update(self, instance, validated_data):
    # Exclude 'user' from validated_data to avoid unintentional username checks
      user_data = validated_data.pop('user', None)

    # Check if user_data is not None and username is not 'None'
      if user_data and user_data.get('username') != 'None':
          instance.user.username = user_data.get('username', instance.user.username)
      instance.user.email = user_data.get('email', instance.user.email)
      instance.user.save()

    # Update Utilisateur fields
      instance.first_name = validated_data.get('first_name', instance.first_name)
      instance.family_name = validated_data.get('family_name', instance.family_name)

    # Save Utilisateur instance
      instance.save()

      return instance
"""