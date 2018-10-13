from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import status
from .models import AccountToken

class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # リクエストヘッダからトークン文字列を取得
        token_str = request.META.get('HTTP_AUTHORIZATION')
        if not token_str or not token_str.startswith('Token '):
            # リクエストヘッダにトークンが含まれない場合はエラー
            raise exceptions.AuthenticationFailed({'message': 'リクエストヘッダにトークンが含まれていません。'})

        token_str = token_str[6:]
        print(token_str)

        # トークン文字列からトークンを取得する
        token = AccountToken.get(token_str)
        if token == None:
            # トークンが取得できない場合はエラー
            raise exceptions.AuthenticationFailed({'message': 'トークンが不正です。'})

        # トークンが取得できた場合は、有効期間をチェック
        if not token.check_valid_token():
            # 有効期限切れの場合はエラー
            raise exceptions.AuthenticationFailed({'message': 'トークンが有効期限切れです。'})

        # トークンが有効な場合は、アクセス日時を更新
        token.update_access_datetime()
        return (token.user_id, None)