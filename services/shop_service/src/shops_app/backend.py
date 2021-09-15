import jwt

from django.conf import settings

from rest_framework import authentication, exceptions


class RemoteUser:
    def __init__(self, id):
        self.id = id
        self._is_superuser = False

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_superuser(self):
        return self._is_superuser

    @is_superuser.setter
    def is_superuser(self, bool):
        if bool is True:
            self._is_superuser = True

    @property
    def is_staff(self):
        return self._is_superuser


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        """
        The `authenticate` method is called on every request regardless of
        whether the endpoint requires authentication. 
        `authenticate` has two possible return values:
        1) `None` - We return `None` if we do not wish to authenticate. Usually
                    this means we know authentication will fail. An example of
                    this is when the request does not include a token in the
                    headers.
        2) `(user, token)` - We return a user/token combination when 
                             authentication is successful.
                            If neither case is met, that means there's an error 
                            and we do not return anything.
                            We simple raise the `AuthenticationFailed` 
                            exception and let Django REST Framework
                            handle the rest.
        """
        request.user = None

        # `auth_header` should be an array with two elements:
        # 1) the name of the authentication header (in this case, "Bearer")
        # 2) the JWT that we should authenticate against.
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # Invalid token header. No credentials provided.
            # Do not attempt to authenticate.
            return None

        elif len(auth_header) > 2:
            # Invalid token header. The Token string should not contain spaces.
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            # The auth header prefix is not what we expected.
            # Do not attempt to authenticate.
            return None

        # if all goes well pass the actual credentials authentication to the method below.
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Try to authenticate the given credentials. If authentication is
        successful, return the user and token. If not, throw an error.
        """
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            # User.objects.get(pk=payload['id'])
            user = RemoteUser(id=payload['user_id'])
            user.is_superuser = payload['is_superuser']
            # we should update payload to hold super_user status
        except:
            # we would never enter this block ideally
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
