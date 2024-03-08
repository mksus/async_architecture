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


CLIENT_ID = 'EsYE2kFH3sTNavemPwgpybKOGFEAIakokvSyVxDc'
CLIENT_SECRET = 'S3SvHULyFNyE3pQGqKVxX9J7a1AQAcALtvFDxBC4IyROEuQ6Gy2yNQzBuWLjwSRtU0kiaYbs1aIkB7BzAZ4VUtNG1Yux58DRsDADPjlojvcehv9H7lNZfzKRPXUNzhoG'
REDIRECT_URL = 'http://localhost:8000/users/auth_callback'


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')


# авторизация через oauth backend
@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)


def auth_via_provider(request, *args, **kwargs):
    code_verifier = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))

    print(code_verifier)

    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')

    # todo сохранить verifier и challenge в какую-то oauth сессию
    # todo отправить обратно code_challenge

    auth_url = f'http://127.0.0.1:8000/o/authorize/?response_type=code&code_challenge={code_challenge}&code_challenge_method=S256&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URL}'

    return redirect(to=auth_url)


def auth_callback(request, *args, **kwargs):
    print(request.GET)
    code = request.GET.get('code')

    # todo вытянуть code_verifier из сессии

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code_verifier': '21ROLG20SYP7H2YRW15G5I3PJ4IEK0SATFNQWH3D4D05AEYGU8Y4LY3NO5H8AWHRC7J5V3OQJHW6L3N99FWTQLT6YA5DF0LO7VWEGLRAUHS7OKTRO', # store somewhere code verifier
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
    return HttpResponse('STUB', status=200)
