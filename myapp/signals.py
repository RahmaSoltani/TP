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
import json
from elasticsearch import Elasticsearch

es = Elasticsearch(['localhost:9200'])  # Elasticsearch client

@receiver(post_save)
def update_document(sender, **kwargs):
    # Your existing code to update documents in Elasticsearch
    
    # Serialize index configuration
    index_config = es.indices.get_settings(index='article')
    index_mapping = es.indices.get_mapping(index='article')

    # Write index configuration to JSON file
    with open('index.json', 'w') as json_file:
        json.dump({'settings': index_config, 'mappings': index_mapping}, json_file)

@receiver(post_delete)
def delete_document(sender, **kwargs):
    # Your existing code to delete documents in Elasticsearch
    
    # Serialize index configuration
    index_config = es.indices.get_settings(index='article')
    index_mapping = es.indices.get_mapping(index='article')

    # Write index configuration to JSON file
    with open('../../Database/index_config.json', 'w') as json_file:
        json.dump({'settings': index_config, 'mappings': index_mapping}, json_file)



# Import the required module
import json

# Load and parse the JSON file
with open('../index.json') as f:
    indexes_config = json.load(f)

# Access index configurations
articles_index_config = indexes_config.get('articles')
