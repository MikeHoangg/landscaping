from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from core import views

urlpatterns = [
    path('', views.ActionsBySeasonsView.as_view(), name='actions_by_season'),
    path('admin/', admin.site.urls),
]

urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
