from oauth2_provider.oauth2_validators import AccessToken

from rest_framework import status

from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.logic import get_company_profile
from accounting.models import Transaction
from accounting.serializers import TransactionSerializer


class TransactionList(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['balance:read']
    allowed_methods = ['get']

    def get(self, request, *args, **kwargs):
        token = AccessToken.objects.get(token=request.auth)
        scopes = token.scope

        if 'role:employer' in scopes.split():
            queryset = Transaction.objects.filter(assign=token.user.profile)
        else:
            company_profile = get_company_profile()
            queryset = Transaction.objects.filter(assign=company_profile)
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetBalance(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['balance:read']
    allowed_methods = ['get']

    def get(self, request, *args, **kwargs):
        token = AccessToken.objects.get(token=request.auth)
        scopes = token.scope

        if 'role:employer' in scopes.split():
            balance = token.user.profile.balance
        else:
            balance = get_company_profile().balance
        return Response({'balance': balance}, status=status.HTTP_200_OK)