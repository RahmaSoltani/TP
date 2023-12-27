from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from myapp.views import ExtractTextFromPDFView

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
    path('search/', views.ArticleDocViewSet.as_view({'get': 'list'}), name='article-search'),
    path('logout/', views.login, name='logout'),
    path('extract-text-from-pdf/', ExtractTextFromPDFView.as_view(), name='extract-text-from-pdf'),
#    path('extract_pdf_content/', views.extract_first_word_from_pdf_url, name='extract-pdf-content'),
]