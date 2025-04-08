from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def home(request):
    return JsonResponse({"message": "Bienvenue sur l'API GamerZone !"}, status=200)

urlpatterns = [
    path('', home),  # Ajoutez cette ligne
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/contact/', include('messages_users.urls')),   
    path('api/blogs/', include('blogsApp.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
