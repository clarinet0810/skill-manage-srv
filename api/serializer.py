from rest_framework import serializers
from .models import TblPerson

class TblPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblPerson
        fields = ('last_name', 'last_name_kana')

