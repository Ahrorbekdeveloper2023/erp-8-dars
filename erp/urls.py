from django.urls import path
from .views import LoginView, RegisterView, ProfileView, UpdateProfileView, StudentView, delete

app_name = 'erp'


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update/', UpdateProfileView.as_view(), name='update'),
    path('student/', StudentView.as_view(), name='student'),
    path('delete/<int:id>/', delete, name='delete'),

]