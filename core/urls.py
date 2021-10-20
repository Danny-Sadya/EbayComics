from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from dashboard.views import dashboard_control, delete_snipe, edit_snipe

urlpatterns = [
    path('accounts/login/', LoginView.as_view(template_name='login.html')),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('api/', include('api.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

