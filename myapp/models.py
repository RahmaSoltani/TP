from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


class Moderateur (models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)    
  first_name=models.CharField(null=True,unique=True,max_length=50)
  family_name=models.CharField(null=True,unique=True,max_length=50)

class Admin(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)    
  first_name=models.CharField(null=False,unique=True,max_length=50)
  family_name=models.CharField(null=False,unique=True,max_length=50)

class Author(models.Model):
    name = models.CharField(max_length=100)

class Institution(models.Model):
    name = models.CharField(max_length=100)

class Keyword(models.Model):
    name = models.CharField(max_length=50)

class Reference(models.Model):
    citation = models.TextField()

class Article(models.Model):
    title = models.CharField(max_length=100)
    abstract = models.TextField()
    authors = models.ManyToManyField(Author)
    institutions = models.ManyToManyField(Institution)
    keywords = models.ManyToManyField(Keyword)
    text = models.TextField(null=True)
  #   text = models.TextField()
    pdf_url = models.URLField()
    references = models.ManyToManyField(Reference)
    date_created = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['-date_created']

class Utilisateur(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name=models.CharField(null=True,unique=True,max_length=50)
    family_name=models.CharField(null=True,unique=True,max_length=50)
#   favoris=models.ManyToManyField(documents.ArticleDocument,default=None)

