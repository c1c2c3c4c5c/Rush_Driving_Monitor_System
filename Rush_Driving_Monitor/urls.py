from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from DrivingMonitor import settings
from DrivingMonitor.views import AuthenticationViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', AuthenticationViews.login, name='login'),
    path('register/', AuthenticationViews.register, name='register'),
    path('logout/', AuthenticationViews.logout, name='logout'),
    path('', include('Tracker.urls'))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
