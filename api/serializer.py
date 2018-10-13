from rest_framework import serializers
from .models import TblPerson

class LoginSerializer(serializers.Serializer):
    email=serializers.CharField(help_text='ログインユーザーのメールアドレス')
    password=serializers.CharField(help_text='ログインパスワード')

class TblPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblPerson
        fields = ('last_name', 'last_name_kana')

