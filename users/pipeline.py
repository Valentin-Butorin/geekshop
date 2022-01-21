import requests
from django.conf import settings
from social_core.exceptions import AuthForbidden
from users.models import UserProfile
from datetime import datetime


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    base_url = 'https://api.vk.com/method/users.get/'

    fields_for_request = ['bdate', 'sex', 'about', 'photo_400_orig']
    params = {
        'fields': ','.join(fields_for_request),
        'access_token': response['access_token'],
        'v': settings.API_VERSION
    }

    api_response = requests.get(base_url, params=params)

    if api_response.status_code != 200:
        return

    api_data = api_response.json()['response'][0]

    if 'sex' in api_data:
        if api_data['sex'] == 1:
            user.userprofile.gender = UserProfile.FEMALE
        elif api_data['sex'] == 2:
            user.userprofile.gender = UserProfile.MALE
        else:
            user.userprofile.gender = UserProfile.UNKNOWN

    if 'about' in api_data:
        user.userprofile.about_me = api_data['about']

    if 'bdate' in api_data:
        bdate = datetime.strptime(api_data['bdate'], '%d.%m.%Y').date()
        today = datetime.now().date()

        age = today.year - bdate.year
        if (today.month, today.day) < (bdate.month, bdate.day):
            age -= 1

        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        user.age = age

    if 'photo_400_orig' in api_data:
        photo_url = api_data['photo_400_orig']
        if photo_url != 'https://vk.com/images/camera_400.png':
            filename = photo_url[:photo_url.index('?')].split('/')[-1]
            image_path = 'users_images/' + filename

            with open(f'{settings.MEDIA_ROOT}/{image_path}', 'wb') as f:
                f.write(requests.get(photo_url, stream=True).content)

            user.image = image_path

    user.save()
    user.userprofile.save()

