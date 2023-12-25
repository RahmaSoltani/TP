from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.apps import DEDConfig
from .models import Article
from .documents import ArticleDocument, custom_index_name
from django_elasticsearch_dsl.registries import registry

DEDConfig()
"""
@receiver(post_save, sender=Article)
@receiver(post_delete, sender=Article)
def update_article_index(sender, instance, **kwargs):
    article_document = ArticleDocument(meta={"id": str(instance.pk)})
    article_document.title = instance.title
    article_document.abstract = instance.abstract
    # Set other fields as needed

    article_document.save(index=custom_index_name)
"""
@receiver(post_save)
def update_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']

    if app_label == 'articles':
        if model_name == 'article':
            instances = instance.article.all()
            for _instance in instances:
                registry.update(_instance)


@receiver(post_delete)
def delete_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']

    if app_label == 'articles':
        if model_name == 'article':
            instances = instance.article.all()
            for _instance in instances:
                registry.update(_instance)