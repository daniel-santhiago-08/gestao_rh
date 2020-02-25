from django.urls import path
from .views import home, template, sb_admin


urlpatterns = [
    path('', home, name='home' ),
    path('template/', template, name='template' ),
    # path('sb-admin/', sb_admin, name='sb-admin' ),
]