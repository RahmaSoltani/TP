from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.apps import DEDConfig
from .models import Article
from .documents import ArticleDocument, custom_index_name

DEDConfig()

@receiver(post_save, sender=Article)
@receiver(post_delete, sender=Article)
def update_article_index(sender, instance, **kwargs):
    ArticleDocument().update(instance, index=custom_index_name)