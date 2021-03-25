from django.urls import path
from .views import CreateOrganizationView

app_name = 'organisation'

urlpatterns = [
	path('create', CreateOrganizationView.as_view(), name='create')
]
