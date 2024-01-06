from django.contrib import admin

# Register your models here.


# Register your models here.
from . import models  # Import your models here

admin.site.register(models.Admin)

admin.site.register(models.Utilisateur)
admin.site.register(models.Moderateur)

admin.site.register(models.Article)
admin.site.register(models.Author)
admin.site.register(models.Institution)
admin.site.register(models.Keyword)
admin.site.register(models.Reference)
