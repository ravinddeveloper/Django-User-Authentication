
from django.urls import path,include
from ecomapp import views
urlpatterns = [
    path('',views.index,name="index"),
    path('up-comming-events/',views.up_events,name="events"),
    path('about-us/',views.about,name="about"),
    path('our-team/',views.team,name="team"),
    path('Available-batch/',views.batch,name="batch"),
    path('contact-us/',views.contact,name="contact"),
    
]