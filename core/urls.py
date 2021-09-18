from django.urls import path

from core.views import HomepageView, MovieDetailView, ActorDetailView

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('movie/<int:pk>', MovieDetailView.as_view(), name='movie-detail'),
    path('actor/<int:pk>', ActorDetailView.as_view(), name='actor-detail'),
]
