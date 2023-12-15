from django.urls import path,include
from account import views
urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.handle_login,name="login"),
    path('logout/',views.handlelogout,name="logout"),
    path('activate/<uidb64>/<token>',views.Activate.as_view(),name="activate"),
    path('reset-password-mail/',views.resetPassword.as_view(),name="reset-password"),
    path('new-password/<uidb64>/<token>',views.setNewPassword.as_view(),name="new-password"),

    
]