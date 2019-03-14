"""glasgowgems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from gems import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^add-gem/$', views.add_gem, name='add_gem'),
    url(r'^contact-us/$', views.contact_us, name='contact_us'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
		views.show_category, name='show_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<gem_name_slug>[\w\-]+)/$',
        views.show_gem, name='show_gem'),
    url(r'^sign_up/$',views.sign_up,name="sign_up"),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
     #==========================================================================
     # FUTURE ADDS
     # url(r'^profile/$', views.profile, name='profile'),
     # url(r'^sign-up/$', views.sign_up, name='sign_up'),
     # url(r'^search-results/$', views.search_results, name='search_results')
     #==========================================================================
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
