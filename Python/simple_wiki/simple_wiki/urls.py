from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [url(r'^polls/', include('polls.urls')),
               url(r'^echo',include('echo.urls')),
               url(r'^admin/',admin.site.urls),]

