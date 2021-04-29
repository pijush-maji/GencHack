from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='home'),
    path('enyc/',views.enyc,name='enyc'),
    path('deyc/',views.deyc,name='deyc'),
    
    # path('done/',views.done,name='done'),
    # path('del/',views.dele,name='del')
]

urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)