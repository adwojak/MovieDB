from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from moviesapp.views import (
    DeleteUserView,
    RegisterViewSet,
    MoviesViewSet,
)


router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'movies', MoviesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('delete-user/', DeleteUserView.as_view(), name='delete-user')
]
