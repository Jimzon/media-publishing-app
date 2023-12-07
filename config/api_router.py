from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from company_publishing.articles.api.views import ArticleViewSet
from company_publishing.companies.api.views import CompanyViewSet
from company_publishing.users.api.views import LoginAPIView, SignupAPIView, UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("articles", ArticleViewSet)
router.register("companies", CompanyViewSet)
router.register("users", UserViewSet)


app_name = "api"
urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("signup/", SignupAPIView.as_view(), name="signup"),
] + router.urls
