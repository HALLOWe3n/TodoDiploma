from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import login_redirect


urlpatterns = [
    url(r"^$", login_redirect, name="login_redirect"),
    url(r"^admin/", admin.site.urls),
    url(r"^todo/", include("todo.urls", namespace="todo")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
