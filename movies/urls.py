from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from moviesapp.views import (
    CommentsViewSet,
    DeleteUserView,
    RatingsViewSet,
    RegisterViewSet,
    MoviesViewSet,
    TopMoviesView,
)


router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'ratings', RatingsViewSet)
router.register(r'movies', MoviesViewSet)
router.register(r'comments', CommentsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('delete-user/', DeleteUserView.as_view(), name='delete-user'),
    path('top/', TopMoviesView.as_view(), name='top-movies'),
]
