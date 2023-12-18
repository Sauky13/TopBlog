from django.conf import settings
from django.urls import path
from . import views
from .views import index, LoginViewUser, profile, UserRegister, RegisterDone, logout_view
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
                  path('', index, name='index'),
                  path('accounts/login', LoginViewUser.as_view(), name='login'),
                  path('accounts/login', LoginViewUser.as_view(), name='login'),
                  path('logout/', logout_view, name='logout'),
                  path('register/', UserRegister.as_view(), name='register'),
                  path('register/done/', RegisterDone.as_view(), name='register_done'),
                  path('accounts/profile/', profile, name='profile'),
                  path('edit/', views.edit_user, name='edit_user'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
