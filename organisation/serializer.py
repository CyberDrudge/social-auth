from rest_framework import serializers
from .models import Organisation


class SocialSerializer(serializers.Serializer):
	provider = serializers.CharField(max_length=255, required=True)
	access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)


class OrganisationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Organisation
		fields = '__all__'

