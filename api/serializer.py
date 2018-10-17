from rest_framework import serializers
from .models import TblPerson

class LoginSerializer(serializers.Serializer):
    email=serializers.CharField(help_text='ログインユーザーのメールアドレス')
    password=serializers.CharField(help_text='ログインパスワード')

class TblPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblPerson
        fields = (
            'user_id', 'last_name', 'last_name_kana', 'first_name', 'first_name_kana', 'initial', 'birthday',
            'nearest_station', 'health', 'company_id')

