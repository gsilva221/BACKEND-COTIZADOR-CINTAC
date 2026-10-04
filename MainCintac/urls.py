from django.urls import path
from MainCintac.views import principal

urlpatterns = [
    path('', principal),
]