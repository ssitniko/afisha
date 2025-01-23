
from django.urls import path
from movie_app import views

urlpatterns = [
    # path('', views.movie_list_api_view),
    path('', views.MovieListCreateAPIView.as_view()),
    # path('directors/', views.director_list_api_view),
    path('directors/', views.DirectorListAPIView.as_view()),
    # path('reviews/', views.review_list_api_view),
    path('reviews/', views.ReviewListAPIView.as_view()),
    # path('<int:id>/', views.movie_detail_api_view),
    path('<int:id>/', views.MovieDetailAPIView.as_view()),
    # path('directors/<int:id>/', views.director_detail_api_view),
    path('directors/<int:id>/', views.DirectorDetailAPIView.as_view()),
    # path('reviews/<int:id>/', views.review_detail_api_view),
    path('reviews/<int:id>/', views.ReviewDetailAPIView.as_view()),
    path('search_words/', views.SearchWordsViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('search_words/<int:pk>', views.SearchWordsViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
        }))
]