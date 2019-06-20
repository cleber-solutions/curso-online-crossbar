from django.contrib import admin
from django.conf.urls import url, include


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', admin.site.urls),

    # URLs properly prefixed with API version:
    # url(r'^v1/aws/', include('apps.aws.urls')),
]
