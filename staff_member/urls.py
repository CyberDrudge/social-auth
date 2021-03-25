from django.urls import path
from .views import AddStaffMemberView, ListUserOrganizationView

app_name = 'staff_member'

urlpatterns = [
	path('add', AddStaffMemberView.as_view(), name='create'),
	path('organisations', ListUserOrganizationView.as_view(), name='list')
]
