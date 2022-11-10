import os
import json
import jwt
from jwt import PyJWKClient
from jwt import InvalidTokenError
from jwt.algorithms import RSAAlgorithm
import requests

from cryptography.hazmat.primitives import serialization
from django.core.cache import caches
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions

from api.models.User import User
from api.models.UserCreationRequest import UserCreationRequest
from api.services.KeycloakAPI import map_user
from tfrs.settings import WELL_KNOWN_ENDPOINT

cache = caches['keycloak']

class UserAuthentication(authentication.BaseAuthentication):
    """
    Class to handle authentication when after logging into keycloak
    """

    def refresh_jwk(self):
        oidc_response = requests.get(WELL_KNOWN_ENDPOINT)
        jwks_uri = json.loads(oidc_response.text)['jwks_uri']
        self.jwks_uri = jwks_uri
        certs_response = requests.get(jwks_uri)
        jwks = json.loads(certs_response.text)
        self.jwks = jwks

    def __init__(self):
        self.refresh_jwk()

    def authenticate(self, request):
        """Verify the JWT token and find the correct user in the DB"""

        if not settings.KEYCLOAK['ENABLED']:
            # fall through
            return None

        auth = request.META.get('HTTP_AUTHORIZATION', None)

        if not auth:
            raise exceptions.AuthenticationFailed(
                'Authorization header required')

        try:
            scheme, token = auth.split()
        except ValueError:
            raise exceptions.AuthenticationFailed(
                'Invalid format for authorization header')
        if scheme != 'Bearer':
            raise exceptions.AuthenticationFailed(
                'Authorization header invalid'
            )

        if not token:
            raise exceptions.AuthenticationFailed(
                'No token found'
            )

        user_token = None
        token_validation_errors = []

        jwks_client = jwt.PyJWKClient(self.jwks_uri)

        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)
        except Exception as error:
            print(error)

        try:
            user_token = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=settings.KEYCLOAK['AUDIENCE'],#"sso-test-2-2",
                options={"verify_exp": True},
            )
        except (jwt.InvalidTokenError, jwt.ExpiredSignature, jwt.DecodeError) as exc:
            print(str(exc))
            token_validation_errors.append(exc)
            raise Exception(str(exc))

        if not user_token:
            raise exceptions.AuthenticationFailed(
                'No successful decode of user token. Exceptions occurred: {}',
                '\n'.join([str(error) for error in token_validation_errors])
            )

        # Check for existing mapped user
        if 'preferred_username' in user_token:
            print(user_token['preferred_username'])
            try:
                user = User.objects.get(keycloak_user_id=user_token['preferred_username'])
                print("user exists", user)
                return user, None
            except User.DoesNotExist: 
                print("User does not exist, falling through")
                pass
        
        # fall through to here if no mapped user is found
        if 'email' in user_token:
            creation_request = UserCreationRequest.objects.filter(
                keycloak_email__iexact=user_token['email']
            )

            if not creation_request.exists():
                print("No User with that email exists.")
                raise exceptions.AuthenticationFailed(
                    "No User with that email exists.")

            user_creation_request = creation_request.first()
            print('creation_request', creation_request)

            # map keycloak user to tfrs user
            user = user_creation_request.user
            print("user", user)
            user.keycloak_user_id = user_token['preferred_username']
            if user_token['display_name']:
                user._display_name = user_token['display_name']
            user.save()

            user_creation_request.is_mapped = True
            user_creation_request.save()
        else:
            raise exceptions.AuthenticationFailed(
                'preffered_username or email is required in jwt payload')
        
        try:
            user = User.objects.get(keycloak_user_id=user_token['preferred_username'])
            if not user.is_active:
                raise exceptions.AuthenticationFailed('User is not active')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User does not exist')

        return user, None
