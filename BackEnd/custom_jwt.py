import jwt
import uuid
import warnings

from calendar import timegm
import datetime as date

from datetime import datetime
from django.conf import settings

from rest_framework_jwt.compat import get_username
from rest_framework_jwt.compat import get_username_field
from rest_framework_jwt.settings import api_settings
import json
from socialNetwork.models import ProfileModel


def jwt_payload_handler(user):
    username_field = get_username_field()
    username = get_username(user)

    warnings.warn(
        'The following fields will be removed in the future: '
        '`email` and `user_id`. ',
        DeprecationWarning
    )

    expiry_date = datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA

    prof=ProfileModel.objects.get(user__pk=user.pk)
    name = prof.name
    profilePic = settings.BASE_URL + prof.image.url
            
    payload = {
        'user_id': user.pk,
        'username': username,
        'exp': expiry_date,
        'name': name,
        'pic':profilePic
    }

    if hasattr(user, 'email'):
        payload['email'] = user.email
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    payload[username_field] = username

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    # print(groupsRecieved.data[0])
    # payload['position']=groupsRecieved[0]['name']

    return payload
