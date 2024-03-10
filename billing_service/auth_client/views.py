from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
from django.shortcuts import redirect
import random
import string
import base64
import hashlib
import requests


# Create your views here.

CLIENT_ID = '7lAOlZNDi3LegSqIKUku2vIAXweRsCNqn3Z4nTbX'
CLIENT_SECRET = 'QNXmRUbC9BR2FpuVSGFoCYYeaRGD1bMWXA5BAeS9PJoeOMPItu2DPMCYhBpFef0DGQluwlM2HUupxuSZaHlv9LWVel7qZtn5T5TKSidUC8LhzkI2iLB0mjJ7lmiDNCfX'
REDIRECT_URL = 'http://localhost:8002/auth_client/auth_callback'

# should be new for each session, stored here for quickness
CODE_VERIFIER = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))


# это вью для кнопки "авторизоваться через oauth"
def auth_via_provider(request, *args, **kwargs):

    code_challenge = hashlib.sha256(CODE_VERIFIER.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')

    # todo сохранить verifier и challenge в какую-то oauth сессию
    # todo отправить обратно code_challenge

    auth_url = f'http://127.0.0.1:8000/o/authorize/?response_type=code&code_challenge={code_challenge}&code_challenge_method=S256&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URL}'

    return redirect(to=auth_url)


# callback, который ловит токен и сеттит его в браузер
def auth_callback(request, *args, **kwargs):
    print(request.GET)
    code = request.GET.get('code')

    # todo вытянуть code_verifier из сессии

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code_verifier': CODE_VERIFIER,
        'redirect_uri': REDIRECT_URL,
        'grant_type': 'authorization_code',
        'code': code,
    }

    response = requests.post(
        'http://127.0.0.1:8000/o/token/',
        data=data,
    )
    print(response)
    print(response.text)
    access_token = response.json().get('access_token')
    return HttpResponse(f'access token should be set to frontend storage {access_token}', status=200)
