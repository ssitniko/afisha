from django.urls import path
from users import views

urlpatterns = [
    path('registration/', views.register_api_view),
    path('authorization/', views.auth_api_view),
    path('confirm/', views.confirm_api_view),

]