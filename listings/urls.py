from django.conf.urls import url
from django.urls import path
from listings.views import UnitView

app_name="listings"

urlpatterns = [
    path('units/', UnitView.as_view(), name="units")
]