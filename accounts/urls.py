from django.urls import path
from .import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-account/', views.my_account, name='my_account'),
    path('edit-account/', views.edit_account, name='edit_account'),
]
