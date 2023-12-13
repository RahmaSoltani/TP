
from django_elasticsearch_dsl.registries import registry

from django_elasticsearch_dsl import Document, Index, fields
from .models import Article

@registry.register_document
class ArticleDocument(Document):
    title = fields.TextField()
    abstract = fields.TextField()
    pdf_url = fields.KeywordField()
    date_created = fields.DateField()

    authors = fields.NestedField(properties={
        'name': fields.TextField(),
    })

    institutions = fields.NestedField(properties={
        'name': fields.TextField(),
    })

    keywords = fields.NestedField(properties={
        'name': fields.TextField(),
    })

    references = fields.NestedField(properties={
        'citation': fields.TextField(),
    })

    class Index:
        name = 'article'
    class Django:
        model=Article

"""
class ArticleDocument(Document):
    title = fields.TextField()
    abstract = fields.TextField()
    pdf_url = fields.Keyword()
    date_created = fields.Date()

    authors = fields.Nested(properties={'name': fields.TextField()})
    institutions = fields.Nested(properties={'name': fields.TextField()})
    keywords = fields.Nested(properties={'name': fields.TextField()})
    references = fields.Nested(properties={'citation': fields.TextField()})

    class Index:
        name = 'article_index'

# Define the Django class outside ArticleDocument
    class Django:
      model = Article


class ArticleDocument(Document):
    title = Text()
    abstract = Text()
    pdf_url = Keyword()
    date_created = Date()

    authors = Nested(
        properties={'name': Text()}
    )

    institutions = Nested(
        properties={'name': Text()}
    )

    keywords = Nested(
        properties={'name': Text()}
    )

    references = Nested(
        properties={'citation': Text()}
    )

    class Index:
        name = 'article_index'

    class Django : 
        model=models.Article
"""