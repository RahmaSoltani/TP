from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


class Moderateur (models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)    
  first_name=models.CharField(null=True,unique=True,max_length=50)
  family_name=models.CharField(null=True,unique=True,max_length=50)
  def __str__(self):
     return str(self.first_name+self.family_name)
class Admin(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)    
  first_name=models.CharField(null=False,unique=True,max_length=50)
  family_name=models.CharField(null=False,unique=True,max_length=50)
  def __str__(self):
     return str(self.first_name+self.family_name)
class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
     return str(self.name)
class Institution(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
     return str(self.name)
class Keyword(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
     return str(self.name)
class Reference(models.Model):
    citation = models.TextField()
    def __str__(self):
     return str(self.citation)
class Article(models.Model):
    title = models.CharField(max_length=100)
    abstract = models.TextField()
    authors = models.ManyToManyField(Author)
    institutions = models.ManyToManyField(Institution)
    keywords = models.ManyToManyField(Keyword)
    text = models.TextField(null=True)
    treated = models.BooleanField(default=False)
    pdf_url = models.CharField(max_length=255)  # Change to CharField for local file paths
    references = models.ManyToManyField(Reference)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return str(self.title)

class Utilisateur(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name=models.CharField(null=True,unique=True,max_length=50)
    family_name=models.CharField(null=True,unique=True,max_length=50)
    favoris=models.ManyToManyField(Article,default=None)
    def __str__(self):
     return str(self.first_name+self.family_name)
