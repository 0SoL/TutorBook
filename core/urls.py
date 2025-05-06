from django.urls import path
from .views import home_page, main_page

urlpatterns = [
    path('', home_page, name='home'),
    path('welcome/', main_page, name='welcome')
]
