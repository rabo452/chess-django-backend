import jwt
from django.conf import settings


def is_access_token_valid(token):
    try:
        # Decode the token using the secret key
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        # Token is valid if decoding succeeds
        return True
    except jwt.ExpiredSignatureError:
        # Token is expired
        return False
    except jwt.InvalidTokenError:
        # Token is invalid
        return False


def get_user_id(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256']).get("user_id")
