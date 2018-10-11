# Generated by Django 2.1.2 on 2018-10-11 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblCareer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('career_no', models.IntegerField(verbose_name='経歴NO')),
                ('start_date', models.DateField(verbose_name='開始日')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='終了日')),
                ('project_name', models.CharField(blank=True, max_length=64, verbose_name='プロジェクト名')),
                ('work_discription', models.TextField(blank=True, max_length=128, verbose_name='作業内容')),
                ('work_type', models.IntegerField(blank=True, null=True, verbose_name='作業区分')),
                ('member_count', models.IntegerField(blank=True, null=True, verbose_name='メンバー数')),
                ('position', models.IntegerField(blank=True, null=True, verbose_name='ポジション')),
                ('nearest_station', models.CharField(blank=True, max_length=32, verbose_name='最寄り駅')),
                ('company_cd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.MstCompany')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_career',
            },
        ),
        migrations.CreateModel(
            name='TblQualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquisition_date', models.DateField(blank=True, null=True, verbose_name='取得年月日')),
                ('qualification_cd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.MstQualification')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_qualification',
            },
        ),
        migrations.RenameField(
            model_name='accounttoken',
            old_name='account',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='tblperson',
            old_name='company',
            new_name='company_cd',
        ),
        migrations.RenameField(
            model_name='tblperson',
            old_name='account',
            new_name='user_id',
        ),
        migrations.AlterModelTable(
            name='tblperson',
            table='tbl_person',
        ),
        migrations.AlterUniqueTogether(
            name='tblqualification',
            unique_together={('user_id', 'qualification_cd')},
        ),
        migrations.AlterUniqueTogether(
            name='tblcareer',
            unique_together={('user_id', 'career_no')},
        ),
    ]