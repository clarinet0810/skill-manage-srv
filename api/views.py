from django.http.response import JsonResponse
from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Account, AccountToken
from .models import TblPerson
from .serializer import TblPersonSerializer, LoginSerializer
from.authentication import TokenAuthentication

import json

class Login(mixins.CreateModelMixin, generics.GenericAPIView):
    """
    スキル管理システムへのログイン処理を提供します。
    Return the given user
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        password = serializer.data['password']

        # メールアドレスからユーザを取得
        if not Account.objects.filter(email=email).exists():
            # 存在しない場合は403を返却
            return JsonResponse({'message': 'ログインに失敗しました。'}, status=403)

        account = Account.objects.get(email=email)

        # パスワードチェック
        if not account.check_password(password):
            # チェックエラー
            return JsonResponse({'message': 'ログインに失敗しました'}, status=403)

        # ログインOKの場合は、トークンを生成
        token = AccountToken.create(account)

        # トークンを返却
        return JsonResponse({'user_id': account.user_id, 'token': token.token})


class PersonViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = TblPersonSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            # スーパーユーザーの場合は全ユーザーの情報を取得
            return TblPerson.objects.all()
        else:
            # スーパーユーザー以外の場合は自分の情報のみ
            return TblPerson.objects.filter(user_id=self.request.user)
    
    def get_permissions(self):
        print('is_superuser = ' + str(self.request.user.is_superuser))
        if self.action == 'create' or self.action == 'destroy':
            # 作成、削除は管理者のみ
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]


class YesMan(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        return JsonResponse({'message': 'Yes'})