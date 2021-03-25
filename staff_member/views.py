from .models import StaffMember
from rest_framework.views import APIView
from rest_framework import status, generics, filters
from rest_framework.response import Response
from organisation.models import Organisation
from organisation.serializer import OrganisationSerializer


# Create your views here.
class AddStaffMemberView(APIView):
	def post(self):
		user = self.request.user
		data = self.request.data
		StaffMember.objects.create(data)
		return Response(status=status.HTTP_201_CREATED)


class ListUserOrganizationView(generics.ListAPIView):
	serializer_class = OrganisationSerializer
	filter_backends = [filters.OrderingFilter]
	ordering = ['-created_at', 'name']

	def get_queryset(self):
		user = self.request.user
		return Organisation.objects.get_by_user(user)
