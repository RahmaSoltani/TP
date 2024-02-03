from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from myapp.views import ExtractionView


router = DefaultRouter()
router.register(r'utilisateur', views.UtilisateurViewSet)
router.register(r'moderateur', views.ModerateurViewSet)
router.register(r'admin', views.AdminViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'search', views.ArticleDocViewSet,basename='search')
router.register(r'article', views.ArticleViewSet)
router.register(r'refrence', views.RefrenceViewSet)
router.register(r'author', views.AuthorViewSet)
router.register(r'institution', views.InstitutionViewSet)
router.register(r'keyword', views.KeywordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login, name='login'),
    path('add-article/', views.add_article_to_favorites, name='login'),
    path('article-details/<int:id>/', views.article_details, name='article_details'),
    path('update-article/<int:id>/', views.update_article, name='update'),
    path('favoris/<int:utilisateur_id>/', views.list_favorite_articles, name='list_favorite_articles'),
    path('search-and-filter/', views.search_and_filter_articles, name='search_and_filter_articles'),
    path('treat-article/<int:article_id>/', views.treat_article, name='treat_article'),
    path('articlee/<int:article_id>/', views.get_article, name='get_article'),

    path('check-favorite-article/<int:user_id>/<int:article_id>/', views.check_favorite_article, name='check_favorite_article'),

    path('search/', views.ArticleDocViewSet.as_view({'get': 'list'}), name='article-search'),
    path('logout/', views.login, name='logout'),
    path('change-password/', views.change_password, name='logout'),
    path('non-treated-articles/', views.non_treated_articles, name='non_treated_articles'),

    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),
    path('send_email/', views.send_email, name='send_email'),
    path('extract/', ExtractionView.as_view(), name='extract'),
    path('extract_pdf_content/', views.extract_specific_sections_from_pdf, name='extract-pdf-content'),
]