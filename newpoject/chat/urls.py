from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('local_chat/', views.Home.as_view()),
    path('login/',views.Register.as_view(), name = "login"),
    path('signup/',views.SignUp.as_view(), name = "signup"),
    path('logout/',views.logout_page,name = "logout"),
    path('addfriend/<int:friend_id>',views.add_friend,name = "addFriend")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
