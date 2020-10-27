"""vetwall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from walloffaces.views import (
    VeteranCreate, home_view, VeteranDetail, donation,
    confirm_donation, contact_us_form, search_results, remembrance_form
)

# from django.contrib.sitemaps.views import sitemap
# from .sitemaps import StaticViewSitemap, EventSitemap

# sitemaps = {"static": StaticViewSitemap, "events": EventSitemap}

admin.site.site_header = "SE PA Veterans Wall of Honor Admin"
admin.site.site_title = "SE PA Veterans Wall of Honor Admin Portal"
admin.site.index_title = "Welcome to the SE PA Veterans Wall of Honor Portal"

urlpatterns = [
    path("cms/", admin.site.urls),
    path("", home_view, name="home"),
    path("wall-of-honor/submit-biography",
         VeteranCreate.as_view(), name="submit_biography"),
    path("wall-of-honor/<int:pk>", VeteranDetail.as_view(), name="vet_detail"),
    path("donate/donation", donation, name="donation"),
    path("donate/confirm_donation", confirm_donation, name="confirm_donation"),
    path("contact_form", contact_us_form, name="contact_us_form"),
    path("wall-of-honor/search", search_results, name="vet_search"),
    path("wall-of-honor/<int:vet_id>/remembrance",
         remembrance_form, name="submit_remembrance"),
    # path("", include("pages.urls")),
    # path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    # path(
    #     "robots.txt",
    #     TemplateView.as_view(template_name="robots.txt",
    #                          content_type="text/plain"),
    # ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
