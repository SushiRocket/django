from django.urls import path
from.import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'notes'

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('category/<int:pk>/',views.CategoryView.as_view(),name='category'),
    path('detail/<int:pk>/',views.DetailView.as_view(),name='detail'),
    path('comment/<int:post_pk>/',views.CommentView.as_view(),name='comment'),
    path('about/',views.AboutView.as_view(),name='about'),
    path('contact/',views.ContactView.as_view(),name='contact_form'),
    path('contact_confirm/',views.ContactConfirmView.as_view(),name='contact_confirm'),
    path('contact_success/', views.ContactSuccessView.as_view(),name='contact_success'),
    path('signup/', views.SignUpView.as_view(),name='signup'),
    path('like/<int:post_pk>/', views.LikeToggleView.as_view(),name='like_toggle'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)