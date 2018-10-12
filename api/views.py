from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Account, AccountToken
from .models import TblPerson
from .serializer import TblPersonSerializer
from.authentication import TokenAuthentication

import json

class Login(APIView):
    def post(self, request, format=None):
        # リクエストボディのJSONを読み込み、メールアドレス、パスワードを取得
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']
        except:
            # JSONの読み込みに失敗
            return JsonResponse({'message': 'Post data injustice'}, status=400)

        # メールアドレスからユーザを取得
        if not Account.objects.filter(email=email).exists():
            # 存在しない場合は403を返却
            return JsonResponse({'message': 'Login failure.'}, status=403)

        account = Account.objects.get(email=email)

        # パスワードチェック
        if not account.check_password(password):
            # チェックエラー
            return JsonResponse({'message': 'Login failure.'}, status=403)

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