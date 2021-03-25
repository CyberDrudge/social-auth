from django.contrib.auth import login
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from requests.exceptions import HTTPError
from rest_framework_jwt.settings import api_settings
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from .serializer import SocialSerializer
from .models import Organisation

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class SocialLoginView(generics.GenericAPIView):
	serializer_class = SocialSerializer
	permission_classes = [permissions.AllowAny]

	def post(self, request):
		"""Authenticate user through the provider and access_token"""
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		provider = serializer.data.get('provider', None)
		strategy = load_strategy(request)

		try:
			backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)

		except MissingBackend:
			return Response({'error': 'Please provide a valid provider'}, status=status.HTTP_400_BAD_REQUEST)
		try:
			access_token = serializer.data.get('access_token')
			user = backend.do_auth(access_token)
		except HTTPError as error:
			return Response({
				"error": {
					"access_token": "Invalid token",
					"details": str(error)
				}
			}, status=status.HTTP_400_BAD_REQUEST)
		except AuthTokenError as error:
			return Response({
				"error": "Invalid credentials",
				"details": str(error)
			}, status=status.HTTP_400_BAD_REQUEST)

		try:
			authenticated_user = backend.do_auth(access_token, user=user)
		except HTTPError as error:
			return Response({
				"error": "invalid token",
				"details": str(error)
			}, status=status.HTTP_400_BAD_REQUEST)

		except AuthForbidden as error:
			return Response({
				"error": "invalid token",
				"details": str(error)
			}, status=status.HTTP_400_BAD_REQUEST)

		if authenticated_user and authenticated_user.is_active:
			login(request, authenticated_user)
			data = {
				"token": jwt_encode_handler(
					jwt_payload_handler(user)
				)}
			response = {
				"name": authenticated_user.name,
				"token": data.get('token')
			}
			return Response(status=status.HTTP_200_OK, data=response)


class CreateOrganizationView(APIView):
	def post(self):
		user = self.request.user
		data = self.request.data
		Organisation.objects.create(data)
		return Response(status=status.HTTP_201_CREATED)
