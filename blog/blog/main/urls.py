from django.conf import settings
from django.urls import path
from . import views
from .views import index, LoginViewUser, profile, UserRegister, RegisterDone, logout_view, create_post, PostDeleteView, \
    PostUpdateView, post_detail, delete_comment
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
                  path('accounts/profile/create-post/', create_post, name='create-post'),
                  path('edit/', views.edit_user, name='edit_user'),
                  path('delete_user/', views.delete_user, name='delete_user'),
                  path('accounts/profile/edit-post/<int:pk>/', PostUpdateView.as_view(), name='edit-post'),
                  path('accounts/profile/delete-post/<int:pk>/', PostDeleteView.as_view(), name='delete-post'),
                  path('post/<int:post_id>/', post_detail, name='post_detail'),
                  path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
