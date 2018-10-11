from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class AccountManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self._create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):

    user_id = models.AutoField('ユーザーID', primary_key=True)
    email = models.EmailField('メールアドレス', unique=True)
    is_staff = models.BooleanField('スタッフ権限', default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FiELDS = []

    def __str__(self):
        return self.email


class AccountToken(models.Model):
    # 紐づくユーザー
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    # アクセストークン
    token = models.CharField(max_length=40)
    # アクセス日時
    access_datetime = models.DateTimeField()

    def __str__(self):
        # メールアドレスとアクセス日時、トークンが見えるようにする。
        dt = timezone.localtime(self.access_datetime).strftime('%Y/%m/%d %H:%M:%S')
        return self.user_id + '(' + dt + ') - ' + self.token


class MstClass(models.Model):
    class_cd = models.IntegerField('区分コード', primary_key=True)
    class_name = models.CharField('区分名', max_length=64)
    type_1 = models.IntegerField('分類1')
    type_2 = models.IntegerField('分類2')
    type_3 = models.IntegerField('分類3')

    class Meta:
        db_table = 'mst_class'
        unique_together = (
            ('type_1', 'type_2', 'type_3'),
        )


class MstCompany(models.Model):
    company_cd = models.IntegerField('企業コード')
    seq_no = models.IntegerField('連番')
    company_name = models.CharField('企業名', max_length=64, unique=True)
    zip_cd = models.CharField('郵便番号', max_length=8, blank=True)
    address = models.CharField('住所', max_length=128, blank=True)
    tel_no = models.CharField('電話番号', max_length=16, blank=True)

    def __str__(self):
        return '(' + str(self.company_cd) +'-' + str(self.seq_no) + ')' + self.company_name

    class Meta:
        db_table = 'mst_company'
        unique_together = (
            ('company_cd', 'seq_no'),
        )


class MstQualification(models.Model):
    qualification_cd = models.IntegerField('資格コード')
    seq_no = models.IntegerField('連番')
    qualification_name = models.CharField('資格名', max_length=64, unique=True)
    class_cd = models.ForeignKey(MstClass, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mst_qualification'
        unique_together = (
            ('qualification_cd', 'seq_no'),
        )


class MstOS(models.Model):
    os_cd = models.IntegerField('OSコード', primary_key=True)
    os_name = models.CharField('OS名', max_length=64, unique=True)
    class_cd = models.ForeignKey(MstClass, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mst_os'



class MstLanguage(models.Model):
    language_cd = models.IntegerField('言語コード', primary_key=True)
    language_name = models.CharField('言語名', max_length=64, unique=True)
    class_cd = models.ForeignKey(MstClass, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mst_language'


class MstTool(models.Model):
    tool_cd = models.IntegerField('ツールコード', primary_key=True)
    tool_name = models.CharField('ツール名', max_length=64, unique=True)
    class_cd = models.ForeignKey(MstClass, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mst_tool'


class MstDB(models.Model):
    db_cd = models.IntegerField('DBコード', primary_key=True)
    db_name = models.CharField('DB名', max_length=64, unique=True)
    class_cd = models.ForeignKey(MstClass, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mst_db'


class TblPerson(models.Model):
    user_id = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    last_name = models.CharField('姓', max_length=16, blank=True)
    last_name_kana = models.CharField('姓かな', max_length=16, blank=True)
    first_name = models.CharField('名', max_length=16, blank=True)
    first_name_kana = models.CharField('名かな', max_length=16, blank=True)
    initial = models.CharField('イニシャル', max_length=3, blank=True)
    birthday = models.DateField('生年月日', blank=True, null=True)
    nearest_station = models.CharField('最寄駅', max_length=32, blank=True)
    health = models.TextField('健康状態', max_length=256, blank=True)
    company_cd = models.ForeignKey(MstCompany, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'tbl_person'


class TblQualification(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    qualification_cd = models.ForeignKey(MstQualification, on_delete=models.CASCADE)
    acquisition_date = models.DateField('取得年月日', blank=True, null=True)

    class Meta:
        db_table = 'tbl_qualification'
        unique_together = (
            ('user_id', 'qualification_cd'),
        )


class TblCareer(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    career_no = models.IntegerField('経歴NO')
    start_date = models.DateField('開始日')
    end_date = models.DateField('終了日', blank=True, null=True)
    project_name = models.CharField('プロジェクト名', max_length=64, blank=True)
    work_discription = models.TextField('作業内容', max_length=128, blank=True)
    work_type = models.IntegerField('作業区分', blank=True, null=True)
    member_count = models.IntegerField('メンバー数', blank=True, null=True)
    position = models.IntegerField('ポジション', blank=True, null=True)
    company_cd = models.ForeignKey(MstCompany, on_delete=models.CASCADE, blank=True, null=True)
    nearest_station = models.CharField('最寄り駅', max_length=32, blank=True)

    class Meta:
        db_table = 'tbl_career'
        unique_together = (
            ('user_id', 'career_no'),
        )  

# class TblCareerOs(models.Model):
#     user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
#     career_no = models.ForeignKey(TblCareer, on_delete=models.CASCADE, )